_metrics = []


def record_request(route: str, status_code: int, response_time: float = None):
    _metrics.append({
        "route": route,
        "status_code": status_code,
        "response_time": response_time,
    })


def get_metrics() -> list:
    return _metrics


def get_error_count() -> int:
    return sum(1 for m in _metrics if m["status_code"] >= 500)
