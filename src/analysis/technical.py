from __future__ import annotations
import numpy as np
import pandas as pd


def sma(data: pd.Series, period: int) -> pd.Series:
    return data.rolling(window=period).mean()


def ema(data: pd.Series, period: int) -> pd.Series:
    return data.ewm(span=period, adjust=False).mean()


def rsi(data: pd.Series, period: int = 14) -> pd.Series:
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = (-delta.where(delta < 0, 0))
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def macd(data: pd.Series) -> tuple[pd.Series, pd.Series, pd.Series]:
    ema12 = ema(data, 12)
    ema26 = ema(data, 26)
    macd_line = ema12 - ema26
    signal_line = ema(macd_line, 9)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def bollinger_bands(data: pd.Series, period: int = 20,
                    std_dev: float = 2.0) -> tuple[pd.Series, pd.Series, pd.Series]:
    middle = sma(data, period)
    std = data.rolling(window=period).std()
    upper = middle + std_dev * std
    lower = middle - std_dev * std
    return upper, middle, lower


def compute_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    close = df["close"] if "close" in df.columns else df["Close"]
    result = df.copy()
    result["MA20"] = sma(close, 20)
    result["MA50"] = sma(close, 50)
    result["MA200"] = sma(close, 200)
    result["RSI"] = rsi(close, 14)
    result["MACD"], result["MACD_Signal"], result["MACD_Hist"] = macd(close)
    result["BB_Upper"], result["BB_Middle"], result["BB_Lower"] = bollinger_bands(close)
    return result
