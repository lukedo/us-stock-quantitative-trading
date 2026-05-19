from __future__ import annotations

class Order:
    def __init__(self, code: str, side: str, quantity: int, price: float,
                 order_type: str = "LIMIT"):
        self.code = code
        self.side = side
        self.quantity = quantity
        self.price = price
        self.order_type = order_type
        self.filled_qty = 0
        self.status = "PENDING"

    @property
    def remaining(self) -> int:
        return self.quantity - self.filled_qty

    @property
    def is_filled(self) -> bool:
        return self.filled_qty >= self.quantity


class OrderBook:
    def __init__(self):
        self.orders: list[Order] = []

    def add_order(self, order: Order):
        self.orders.append(order)

    def get_pending_orders(self, code: str = "") -> list[Order]:
        result = [o for o in self.orders if o.status == "PENDING"]
        if code:
            result = [o for o in result if o.code == code]
        return result
