from datetime import date, timedelta
from pathlib import Path
import sys

import streamlit as st

from src.data import DEFAULT_TICKERS, DataFetchError, fetch_prices
from src.metrics import (
    correlation_matrix,
    cumulative_returns,
    drawdowns,
    log_returns,
    normalize_prices,
    rolling_volatility,
)
from src.plots import (
    correlation_heatmap,
    cumulative_returns_chart,
    drawdown_chart,
    price_chart,
    volatility_chart,
)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))


st.set_page_config(page_title="Financial Time Series Explorer", layout="wide")


@st.cache_data(show_spinner=False)
def load_prices(tickers, start, end, interval):
    return fetch_prices(tuple(tickers), start, end, interval)


st.title("Financial Time Series Explorer")
st.caption(
    "Interactive visualization of prices, returns, volatility, "
    "drawdowns, and correlations."
)

# Sidebar filters
st.sidebar.header("Filters")

today = date.today()
default_start = today - timedelta(days=365 * 3)

start_date = st.sidebar.date_input("Start date", value=default_start)
end_date = st.sidebar.date_input("End date", value=today)

if start_date >= end_date:
    st.sidebar.error("Start date must be before end date.")
    st.stop()

tickers = st.sidebar.multiselect(
    "Tickers",
    options=DEFAULT_TICKERS,
    default=DEFAULT_TICKERS[:2],
)

interval = st.sidebar.selectbox("Frequency", options=["1d", "1wk", "1mo"], index=0)
window = st.sidebar.slider(
    "Rolling window (days)", min_value=10, max_value=120, value=20, step=5
)

if not tickers:
    st.warning("Select at least one ticker.")
    st.stop()

try:
    prices = load_prices(tickers, str(start_date), str(end_date), interval)
except DataFetchError as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

if prices.empty:
    st.warning("No price data available for the selected period.")
    st.stop()

prices = load_prices(tickers, str(start_date), str(end_date), interval)

if prices.empty:
    st.warning("No price data available for the selected period.")
    st.stop()

norm_prices = normalize_prices(prices)
log_rets = log_returns(prices)
cum_rets = cumulative_returns(log_rets)
vol = rolling_volatility(log_rets, window=window)
dd = drawdowns(prices)
corr = correlation_matrix(log_rets)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Prices", "Returns & Volatility", "Drawdowns", "Correlation"]
)

with tab1:
    st.plotly_chart(price_chart(norm_prices), use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(cumulative_returns_chart(cum_rets), use_container_width=True)
    with col2:
        st.plotly_chart(volatility_chart(vol), use_container_width=True)

with tab3:
    st.plotly_chart(drawdown_chart(dd), use_container_width=True)

with tab4:
    st.plotly_chart(correlation_heatmap(corr), use_container_width=True)
    st.dataframe(corr.style.format("{:.2f}"))
