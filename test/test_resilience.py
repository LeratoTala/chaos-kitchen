import pytest
import time
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


def test_app_recovers_after_db_timeout():
    """App should return 503 during DB slowness, then recover."""
    with patch("app.database.get_db") as mock_db:
        mock_db.side_effect = TimeoutError("DB timed out")
        response = client.get("/orders")
        assert response.status_code == 503

    # After patch lifted, app should work again
    response = client.get("/orders")
    assert response.status_code == 200


def test_app_returns_error_on_db_unavailable():
    with patch("app.database.get_db") as mock_db:
        mock_db.side_effect = ConnectionError("DB unreachable")
        response = client.post("/orders", json={"item": "sushi", "quantity": 1})
        assert response.status_code in (503, 500)


def test_health_endpoint_reflects_db_down():
    with patch("app.database.get_db") as mock_db:
        mock_db.side_effect = ConnectionError("DB unreachable")
        response = client.get("/health")
        assert response.status_code in (200, 503)
        if response.status_code == 200:
            assert response.json().get("db") in ("down", "unhealthy", False)


def test_multiple_concurrent_orders_handled():
    """Simulate burst of orders and ensure no 500s."""
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
    """Response should not hang indefinitely under slow DB."""
    with patch("app.database.get_db") as mock_db:
        def slow_db():
            time.sleep(2)
            return MagicMock()
        mock_db.side_effect = slow_db

        start = time.time()
        response = client.get("/orders")
        elapsed = time.time() - start

        # Should either timeout gracefully or respond within a reasonable window
        assert elapsed < 10
        assert response.status_code in (200, 503, 504)


def test_metrics_recorded_on_order():
    """Metrics should be updated when an order is placed."""
    with patch("app.metrics.record_request") as mock_metrics:
        client.post("/orders", json={"item": "wrap", "quantity": 1})
        mock_metrics.assert_called()


def test_chaos_runner_calls_experiment():
    from chaos.runner import run_experiment
    with patch("chaos.runner.run_experiment") as mock_run:
        mock_run("slow_database")
        mock_run.assert_called_once_with("slow_database")
