import pandas as pd
import numpy as np


def normalize_prices(prices: pd.DataFrame) -> pd.DataFrame:
    if prices.empty:
        return prices
    return prices / prices.iloc[0] * 100.0


def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna(how="all")


def log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return np.log(prices / prices.shift(1)).dropna(how="all")


def cumulative_returns(log_rets: pd.DataFrame) -> pd.DataFrame:
    return log_rets.cumsum().apply(np.exp) - 1.0


def rolling_volatility(
    log_rets: pd.DataFrame,
    window: int = 20,
    trading_days: int = 252,
) -> pd.DataFrame:
    vol = log_rets.rolling(window=window).std() * np.sqrt(trading_days)
    return vol.dropna(how="all")


def drawdowns(prices: pd.DataFrame) -> pd.DataFrame:
    if prices.empty:
        return prices
    cum_max = prices.cummax()
    return (prices / cum_max) - 1.0


def correlation_matrix(
    log_rets: pd.DataFrame,
) -> pd.DataFrame:
    return log_rets.corr()