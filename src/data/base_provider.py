from abc import ABC, abstractmethod
import pandas as pd


class DataProvider(ABC):
    @abstractmethod
    def get_stock_quote(self, codes: list[str]) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_history_kline(self, code: str, ktype: str = "1d",
                          start: str = "", end: str = "",
                          count: int = 100) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_option_expiration_dates(self, code: str) -> list[str]:
        pass

    @abstractmethod
    def get_option_chain(self, code: str, start: str = "",
                         end: str = "") -> pd.DataFrame:
        pass
