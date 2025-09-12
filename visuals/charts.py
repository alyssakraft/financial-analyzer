#chart functions (price, bar, radar, etc.)

import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from data.fetcher import (get_stock_object, get_price_history)

def plot_stocks(ticker: str):
    hist = get_price_history(ticker)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name=ticker))
    fig.update_layout(title=f"{ticker} Closing Price (1Y)", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)

def growth_line_chart(ticker, data):
    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=data.index, y=data.values, name = ticker))
    # fig.update_layout(title=f"{ticker} {data.name}", xaxis="Date", yaxis="Percent Growth")
    # st.plotly_chart(fig, use_container_width=True)

    fig = px.line(
        x=data.index,
        y=data.values,
        labels={'x': 'Year', 'y': 'Percent Change'},
        title=f"{ticker} {data.name} Over Time"
    )
    fig.update_layout(yaxis_tickformat=".2%")
    return fig
