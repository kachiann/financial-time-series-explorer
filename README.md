# Financial Time Series Explorer

Interactive Streamlit app to explore financial time series for indices, stocks, and FX, with views on prices, returns, volatility, drawdowns, and correlations.

## Features

- Fetch daily OHLCV data for selected instruments via public APIs.
- Visualize normalized prices and cumulative returns.
- Inspect rolling volatility and drawdown profiles.
- View correlation heatmaps over user-selected windows.
- Filter by date range, instruments, and rolling window size.

## Tech stack

- Python, pandas, NumPy
- Streamlit, Plotly
- yfinance (or similar) for public financial data

## How to run

```bash
git clone <repo-url>
cd financial-time-series-explorer
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Notes

- This project is intended as an educational and portfolio-oriented visualization tool for financial time series, not as trading advice.