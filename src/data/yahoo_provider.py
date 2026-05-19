from __future__ import annotations
import yfinance as yf
import pandas as pd


class YahooProvider:
    def get_stock_quote(self, codes: list[str]) -> pd.DataFrame:
        rows = []
        for code in codes:
            ticker = yf.Ticker(code)
            info = ticker.info
            rows.append({
                "code": code,
                "name": info.get("shortName", ""),
                "price": info.get("regularMarketPrice", info.get("currentPrice", 0)),
                "open": info.get("regularMarketOpen", 0),
                "high": info.get("regularMarketDayHigh", 0),
                "low": info.get("regularMarketDayLow", 0),
                "volume": info.get("regularMarketVolume", 0),
                "market_cap": info.get("marketCap", 0),
                "pe": info.get("trailingPE", 0),
            })
        return pd.DataFrame(rows)

    def get_history_kline(self, code: str, ktype: str = "1d",
                          start: str = "", end: str = "",
                          count: int = 100) -> pd.DataFrame:
        ticker = yf.Ticker(code)
        period = f"{count}d" if not start else None
        df = ticker.history(period=period, start=start, end=end, interval=ktype)
        df = df.reset_index()
        df.columns = [c.lower() for c in df.columns]
        return df

    def get_option_expiration_dates(self, code: str) -> list[str]:
        ticker = yf.Ticker(code)
        return list(ticker.options)

    def get_option_chain(self, code: str, start: str = "",
                         end: str = "") -> pd.DataFrame:
        ticker = yf.Ticker(code)
        expiration_dates = ticker.options
        if not expiration_dates:
            return pd.DataFrame()
        target_dates = [d for d in expiration_dates]
        if start:
            target_dates = [d for d in target_dates if d >= start]
        if end:
            target_dates = [d for d in target_dates if d <= end]
        if not target_dates:
            target_dates = [expiration_dates[0]]
        chains = []
        for exp_date in target_dates[:3]:
            opt = ticker.option_chain(exp_date)
            calls = opt.calls.copy()
            puts = opt.puts.copy()
            calls["option_type"] = "CALL"
            puts["option_type"] = "PUT"
            calls["expiration"] = exp_date
            puts["expiration"] = exp_date
            chains.append(calls)
            chains.append(puts)
        return pd.concat(chains, ignore_index=True) if chains else pd.DataFrame()
