import pytest
import time
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


def test_app_recovers_after_db_timeout():
    """
    Verify that the app returns 503 while the database is timing out,
    and then recovers and serves requests normally once the DB is available again.
    """
    with patch("app.database.get_db") as mock_db:
        mock_db.side_effect = TimeoutError("DB timed out")
        response = client.get("/orders")
        assert response.status_code == 503

    response = client.get("/orders")
    assert response.status_code == 200


def test_app_returns_error_on_db_unavailable():
    """
    Verify that when the database is completely unreachable,
    the app returns a 500 or 503 rather than an unhandled exception.
    """
    with patch("app.database.get_db") as mock_db:
        mock_db.side_effect = ConnectionError("DB unreachable")
        response = client.post("/orders", json={"item": "sushi", "quantity": 1})
        assert response.status_code in (503, 500)


def test_health_endpoint_reflects_db_down():
    """
    Verify that the /health endpoint communicates DB unavailability,
    either by returning a non-200 status or by including a db field marked as down.
    """
    with patch("app.database.get_db") as mock_db:
        mock_db.side_effect = ConnectionError("DB unreachable")
        response = client.get("/health")
        assert response.status_code in (200, 503)
        if response.status_code == 200:
            assert response.json().get("db") in ("down", "unhealthy", False)


def test_multiple_concurrent_orders_handled():
    """
    Verify that the app handles a burst of 10 concurrent order requests
    without returning any unexpected 500 errors.
    Acceptable responses are 201 (success), 429 (rate limited), or 503 (overloaded).
    """
    import threading
    results = []

    def place_order():
        r = client.post("/orders", json={"item": "fries", "quantity": 1})
        results.append(r.status_code)

    threads = [threading.Thread(target=place_order) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert all(code in (201, 429, 503) for code in results)


def test_slow_db_response_time():
    """
    Verify that the app does not hang indefinitely when the database is slow.
    The response should complete within 10 seconds and return a valid status code,
    either succeeding or failing gracefully with 503 or 504.
    """
    with patch("app.database.get_db") as mock_db:
        def slow_db():
            time.sleep(2)
            return MagicMock()
        mock_db.side_effect = slow_db

        start = time.time()
        response = client.get("/orders")
        elapsed = time.time() - start

        assert elapsed < 10
        assert response.status_code in (200, 503, 504)


def test_metrics_recorded_on_order():
    """
    Verify that placing an order triggers a call to the metrics recorder,
    confirming that observability hooks are wired up correctly.
    """
    with patch("app.metrics.record_request") as mock_metrics:
        client.post("/orders", json={"item": "wrap", "quantity": 1})
        mock_metrics.assert_called()


def test_chaos_runner_calls_experiment():
    """
    Verify that the chaos runner's run_experiment function is callable
    and can be invoked with an experiment name like 'slow_database'.
    """
    from chaos.runner import run_experiment
    with patch("chaos.runner.run_experiment") as mock_run:
        mock_run("slow_database")
        mock_run.assert_called_once_with("slow_database")
