from __future__ import annotations
import pandas as pd
from datetime import datetime


class Account:
    def __init__(self, initial_cash: float = 100000.0):
        self.cash = initial_cash
        self.positions: dict[str, dict] = {}
        self.trade_history: list[dict] = []

    @property
    def total_value(self) -> float:
        pos_value = sum(
            p["quantity"] * p["current_price"]
            for p in self.positions.values()
        )
        return self.cash + pos_value

    def open_position(self, code: str, quantity: int, price: float,
                      side: str = "BUY", timestamp: str = ""):
        cost = quantity * price
        if side == "BUY":
            if cost > self.cash:
                raise ValueError(f"现金不足: 需要 {cost}, 可用 {self.cash}")
            self.cash -= cost
            if code not in self.positions:
                self.positions[code] = {"quantity": 0, "avg_cost": 0.0,
                                        "current_price": price}
            pos = self.positions[code]
            total_cost = pos["avg_cost"] * pos["quantity"] + cost
            pos["quantity"] += quantity
            pos["avg_cost"] = total_cost / pos["quantity"]
            pos["current_price"] = price
        else:
            if code not in self.positions or self.positions[code]["quantity"] < quantity:
                raise ValueError(f"持仓不足: {code}")
            pos = self.positions[code]
            pos["quantity"] -= quantity
            self.cash += cost
            if pos["quantity"] == 0:
                del self.positions[code]
        self.trade_history.append({
            "timestamp": timestamp or datetime.now().isoformat(),
            "code": code, "side": side,
            "quantity": quantity, "price": price,
            "value": cost
        })

    def update_prices(self, prices: dict[str, float]):
        for code, price in prices.items():
            if code in self.positions:
                self.positions[code]["current_price"] = price

    def get_unrealized_pl(self) -> float:
        return sum(
            p["quantity"] * (p["current_price"] - p["avg_cost"])
            for p in self.positions.values()
        )

    def summary(self) -> dict:
        return {
            "cash": round(self.cash, 2),
            "positions_value": round(self.total_value - self.cash, 2),
            "total_value": round(self.total_value, 2),
            "unrealized_pl": round(self.get_unrealized_pl(), 2),
            "position_count": len(self.positions),
            "trade_count": len(self.trade_history),
        }
