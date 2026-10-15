import pytest
from unittest.mock import patch, MagicMock


def test_collector_records_request_metric():
    """
    Verify that the collector stores a request metric entry
    when record_request is called with a route and status code.
    """
    from monitor.collector import record_request, get_metrics
    record_request(route="/orders", status_code=201)
    metrics = get_metrics()
    assert any(m["route"] == "/orders" for m in metrics)


def test_collector_records_response_time():
    """
    Verify that the collector captures response time alongside
    the request metric so it is available for analysis.
    """
    from monitor.collector import record_request, get_metrics
    record_request(route="/orders", status_code=200, response_time=0.45)
    metrics = get_metrics()
    assert any(m.get("response_time") == 0.45 for m in metrics)


def test_collector_get_metrics_returns_list():
    """
    Verify that get_metrics always returns a list,
    even when no requests have been recorded yet.
    """
    from monitor.collector import get_metrics
    result = get_metrics()
    assert isinstance(result, list)


def test_collector_tracks_error_rates():
    """
    Verify that the collector correctly identifies and counts
    error responses (5xx status codes) separately from successes.
    """
    from monitor.collector import record_request, get_error_count
    record_request(route="/orders", status_code=503)
    count = get_error_count()
    assert count >= 1


def test_dashboard_loads_metrics():
    """
    Verify that the dashboard module can retrieve metrics from the collector
    without raising an exception, confirming the data pipeline is connected.
    """
    from monitor import dashboard
    with patch("monitor.collector.get_metrics", return_value=[]) as mock_get:
        dashboard.load_metrics()
        mock_get.assert_called_once()


def test_dashboard_handles_empty_metrics():
    """
    Verify that the dashboard handles an empty metrics list gracefully
    without crashing or raising an exception.
    """
    from monitor import dashboard
    with patch("monitor.collector.get_metrics", return_value=[]):
        result = dashboard.load_metrics()
        assert result is not None
