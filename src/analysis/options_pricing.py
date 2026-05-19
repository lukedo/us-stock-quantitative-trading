from __future__ import annotations
import numpy as np
from scipy.stats import norm


def black_scholes_price(s: float, k: float, t: float, r: float,
                        sigma: float, option_type: str = "call") -> float:
    d1 = (np.log(s / k) + (r + 0.5 * sigma ** 2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)
    if option_type.lower() == "call":
        return s * norm.cdf(d1) - k * np.exp(-r * t) * norm.cdf(d2)
    else:
        return k * np.exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)


def calculate_greeks(s: float, k: float, t: float, r: float,
                     sigma: float, option_type: str = "call") -> dict:
    d1 = (np.log(s / k) + (r + 0.5 * sigma ** 2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)
    delta = norm.cdf(d1) if option_type.lower() == "call" else -norm.cdf(-d1)
    gamma = norm.pdf(d1) / (s * sigma * np.sqrt(t))
    vega = s * norm.pdf(d1) * np.sqrt(t) / 100
    theta_call = (-(s * norm.pdf(d1) * sigma) / (2 * np.sqrt(t))
                  - r * k * np.exp(-r * t) * norm.cdf(d2)) / 365
    theta_put = (-(s * norm.pdf(d1) * sigma) / (2 * np.sqrt(t))
                 + r * k * np.exp(-r * t) * norm.cdf(-d2)) / 365
    theta = theta_call if option_type.lower() == "call" else theta_put
    rho = (k * t * np.exp(-r * t) * norm.cdf(d2)) / 100 if option_type.lower() == "call" \
        else (-k * t * np.exp(-r * t) * norm.cdf(-d2)) / 100
    return {
        "delta": round(delta, 4),
        "gamma": round(gamma, 4),
        "vega": round(vega, 4),
        "theta": round(theta, 4),
        "rho": round(rho, 4),
    }


def implied_volatility(market_price: float, s: float, k: float, t: float,
                       r: float, option_type: str = "call",
                       tol: float = 1e-6, max_iter: int = 100) -> float:
    sigma = 0.3
    for _ in range(max_iter):
        price = black_scholes_price(s, k, t, r, sigma, option_type)
        diff = price - market_price
        if abs(diff) < tol:
            return sigma
        vega = s * norm.pdf((np.log(s / k) + (r + 0.5 * sigma ** 2) * t)
                            / (sigma * np.sqrt(t))) * np.sqrt(t)
        if abs(vega) < 1e-12:
            break
        sigma = sigma - diff / vega
    return sigma
