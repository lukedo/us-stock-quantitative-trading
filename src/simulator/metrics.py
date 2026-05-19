import numpy as np
import pandas as pd


def calculate_metrics(trade_history: list[dict],
                      equity_curve: list[float]) -> dict:
    if not trade_history:
        return {}
    total_trades = len(trade_history)
    wins = [t for t in trade_history if t.get("pnl", 0) > 0]
    loss = [t for t in trade_history if t.get("pnl", 0) <= 0]
    win_rate = len(wins) / total_trades if total_trades > 0 else 0
    equity_series = pd.Series(equity_curve)
    returns = equity_series.pct_change().dropna()
    total_return = (equity_series.iloc[-1] / equity_series.iloc[0] - 1) * 100
    sharpe = (returns.mean() / returns.std() * np.sqrt(252)
              if returns.std() > 0 else 0)
    max_drawdown = 0
    peak = equity_series[0]
    for v in equity_series:
        if v > peak:
            peak = v
        dd = (peak - v) / peak * 100
        if dd > max_drawdown:
            max_drawdown = dd
    return {
        "total_return_pct": round(total_return, 2),
        "total_trades": total_trades,
        "win_rate_pct": round(win_rate * 100, 2),
        "sharpe_ratio": round(sharpe, 2),
        "max_drawdown_pct": round(max_drawdown, 2),
    }
