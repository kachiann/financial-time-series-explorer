from functools import lru_cache
from typing import List, Tuple

import pandas as pd
import yfinance as yf

DEFAULT_TICKERS: List[str] = [
    "^GSPC",
    "^GDAXI",
    "^STOXX50E",
    "AAPL",
    "MSFT",
    "SAP.DE",
    "EURUSD=X",
]


class DataFetchError(Exception):
    pass


@lru_cache(maxsize=32)
def fetch_prices(
    tickers: Tuple[str, ...],
    start: str,
    end: str,
    interval: str = "1d",
) -> pd.DataFrame:
    if not tickers:
        return pd.DataFrame()

    try:
        data = yf.download(
            list(tickers),
            start=start,
            end=end,
            interval=interval,
            auto_adjust=True,
            progress=False,
        )
    except Exception as exc:
        raise DataFetchError(str(exc)) from exc

    if data.empty:
        raise DataFetchError("No data returned from provider.")

    # Handle both single-ticker and multi-ticker structures
    if isinstance(data.columns, pd.MultiIndex):
        # First level names like 'Price', 'Volume'
        top_level = data.columns.get_level_values(0)
        if "Price" in top_level:
            close_block = data["Price"]["Close"]
        elif "Adj Close" in top_level:
            close_block = data["Adj Close"]
        elif "Close" in top_level:
            close_block = data["Close"]
        else:
            raise DataFetchError(f"Unexpected multi-index columns: {data.columns}")
        prices = close_block
    else:
        # Flat columns: fall back to standard 'Adj Close' / 'Close'
        if "Adj Close" in data.columns:
            prices = data["Adj Close"]
        elif "Close" in data.columns:
            prices = data["Close"]
        else:
            raise DataFetchError(f"Unexpected columns: {data.columns}")

    if isinstance(prices, pd.Series):
        prices = prices.to_frame()

    prices = prices.dropna(how="all")
    if prices.empty:
        raise DataFetchError("No usable price data after cleaning.")

    prices.index.name = "date"
    return prices
