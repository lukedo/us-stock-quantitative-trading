from __future__ import annotations
from src.simulator.account import Account


class SimulatorEngine:
    def __init__(self, initial_cash: float = 100000.0):
        self.account = Account(initial_cash)

    def buy(self, code: str, quantity: int, price: float, timestamp: str = ""):
        self.account.open_position(code, quantity, price, "BUY", timestamp)

    def sell(self, code: str, quantity: int, price: float, timestamp: str = ""):
        self.account.open_position(code, quantity, price, "SELL", timestamp)

    def update_market(self, prices: dict[str, float]):
        self.account.update_prices(prices)

    def status(self) -> dict:
        return self.account.summary()
