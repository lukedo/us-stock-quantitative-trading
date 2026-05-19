from __future__ import annotations
import pandas as pd
from futu import *
from src.config import OPEND_HOST, OPEND_PORT


class FutuProvider:
    def __init__(self, host: str = OPEND_HOST, port: int = OPEND_PORT):
        self.host = host
        self.port = port
        self._quote_ctx: OpenQuoteContext | None = None

    @property
    def quote_ctx(self) -> OpenQuoteContext:
        if self._quote_ctx is None:
            self._quote_ctx = OpenQuoteContext(host=self.host, port=self.port)
        return self._quote_ctx

    def close(self):
        if self._quote_ctx:
            self._quote_ctx.close()
            self._quote_ctx = None

    def get_stock_quote(self, codes: list[str]) -> pd.DataFrame:
        ret, data = self.quote_ctx.get_market_snapshot(codes)
        if ret != RET_OK:
            raise RuntimeError(f"获取快照失败: {data}")
        return data

    def get_history_kline(self, code: str, ktype: str = "1d",
                          start: str = "", end: str = "",
                          count: int = 100) -> pd.DataFrame:
        kl_map = {
            "1m": KLType.K_1M, "5m": KLType.K_5M, "15m": KLType.K_15M,
            "30m": KLType.K_30M, "60m": KLType.K_60M,
            "1d": KLType.K_DAY, "1w": KLType.K_WEEK, "1M": KLType.K_MON
        }
        kl_type = kl_map.get(ktype, KLType.K_DAY)

        if start and end:
            ret, data, _ = self.quote_ctx.request_history_kline(
                code, start=start, end=end, ktype=kl_type,
                max_count=count, autype=AuType.QFQ
            )
        else:
            ret, data = self.quote_ctx.get_cur_kline(
                code, count, kl_type, AuType.QFQ
            )
        if ret != RET_OK:
            raise RuntimeError(f"获取K线失败: {data}")
        return data

    def get_realtime_quote(self, codes: list[str]) -> pd.DataFrame:
        self.quote_ctx.subscribe(codes, [SubType.QUOTE], subscribe_push=False)
        ret, data = self.quote_ctx.get_stock_quote(codes)
        if ret != RET_OK:
            raise RuntimeError(f"获取实时报价失败: {data}")
        return data

    def get_order_book(self, code: str, num: int = 10) -> dict:
        ret, data = self.quote_ctx.get_order_book(code, num=num)
        if ret != RET_OK:
            raise RuntimeError(f"获取摆盘失败: {data}")
        return data

    def get_option_expiration_dates(self, code: str) -> list[str]:
        ret, data = self.quote_ctx.get_option_expiration_date(code)
        if ret != RET_OK:
            raise RuntimeError(f"获取期权到期日失败: {data}")
        return data["strike_time"].tolist()

    def get_option_chain(self, code: str, start: str = "",
                         end: str = "") -> pd.DataFrame:
        ret, data = self.quote_ctx.get_option_chain(code, start=start, end=end)
        if ret != RET_OK:
            raise RuntimeError(f"获取期权链失败: {data}")
        return data
