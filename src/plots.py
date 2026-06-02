import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def price_chart(norm_prices: pd.DataFrame) -> go.Figure:
    df = norm_prices.reset_index().melt(id_vars="date", var_name="ticker", value_name="value")
    fig = px.line(
        df,
        x="date",
        y="value",
        color="ticker",
        title="Normalized prices (start = 100)",
        labels={"date": "Date", "value": "Index level"},
    )
    return fig


def cumulative_returns_chart(cum_rets: pd.DataFrame) -> go.Figure:
    df = cum_rets.reset_index().melt(id_vars="date", var_name="ticker", value_name="value")
    fig = px.line(
        df,
        x="date",
        y="value",
        color="ticker",
        title="Cumulative returns",
        labels={"date": "Date", "value": "Cumulative return"},
    )
    return fig


def volatility_chart(vol: pd.DataFrame) -> go.Figure:
    df = vol.reset_index().melt(id_vars="date", var_name="ticker", value_name="value")
    fig = px.line(
        df,
        x="date",
        y="value",
        color="ticker",
        title="Rolling volatility (annualised)",
        labels={"date": "Date", "value": "Volatility"},
    )
    return fig


def drawdown_chart(dd: pd.DataFrame) -> go.Figure:
    df = dd.reset_index().melt(id_vars="date", var_name="ticker", value_name="value")
    fig = px.area(
        df,
        x="date",
        y="value",
        color="ticker",
        title="Drawdowns",
        labels={"date": "Date", "value": "Drawdown"},
    )
    fig.update_yaxes(tickformat=".0%")
    return fig


def correlation_heatmap(corr: pd.DataFrame) -> go.Figure:
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="Return correlation",
    )
    return fig