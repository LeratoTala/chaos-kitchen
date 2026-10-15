_orders = {}
_next_id = 1


def create_order(item: str, quantity: int) -> dict:
    global _next_id
    order = {"id": _next_id, "item": item, "quantity": quantity}
    _orders[_next_id] = order
    _next_id += 1
    return order


def get_order(order_id: int) -> dict | None:
    return _orders.get(order_id)


def list_orders() -> list:
    return list(_orders.values())
