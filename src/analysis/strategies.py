from __future__ import annotations
import pandas as pd
from src.analysis.technical import sma, rsi, macd


class MovingAverageCrossStrategy:
    def __init__(self, fast: int = 20, slow: int = 50):
        self.fast = fast
        self.slow = slow

    def generate_signal(self, df: pd.DataFrame) -> pd.Series:
        close = df["close"] if "close" in df.columns else df["Close"]
        ma_fast = sma(close, self.fast)
        ma_slow = sma(close, self.slow)
        signal = pd.Series(0, index=df.index)
        signal[(ma_fast > ma_slow) & (ma_fast.shift(1) <= ma_slow.shift(1))] = 1
        signal[(ma_fast < ma_slow) & (ma_fast.shift(1) >= ma_slow.shift(1))] = -1
        return signal


class RsiStrategy:
    def __init__(self, period: int = 14, overbought: float = 70,
                 oversold: float = 30):
        self.period = period
        self.overbought = overbought
        self.oversold = oversold

    def generate_signal(self, df: pd.DataFrame) -> pd.Series:
        close = df["close"] if "close" in df.columns else df["Close"]
        rsi_values = rsi(close, self.period)
        signal = pd.Series(0, index=df.index)
        signal[(rsi_values < self.oversold) & (rsi_values.shift(1) >= self.oversold)] = 1
        signal[(rsi_values > self.overbought) & (rsi_values.shift(1) <= self.overbought)] = -1
        return signal
