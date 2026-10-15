from monitor import collector


def load_metrics() -> list:
    return collector.get_metrics()
