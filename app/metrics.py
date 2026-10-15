from monitor.collector import record_request as _record


def record_request(route: str, status_code: int, response_time: float = None):
    _record(route=route, status_code=status_code, response_time=response_time)
