#chart functions (price, bar, radar, etc.)

import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from data.fetcher import (get_stock_object, get_price_history)

def plot_stocks(ticker: str, ticker2: str = None):
    hist = get_price_history(ticker)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name=ticker))
    if ticker2:
        hist2 = get_price_history(ticker2)
        fig.add_trace(go.Scatter(x=hist2.index, y=hist2['Close'], name=ticker2))
        fig.update_layout(title=f"{ticker} vs. {ticker2} Closing Price (1Y)", xaxis_title="Date", yaxis_title="Price")

    else:
        fig.update_layout(title=f"{ticker} Closing Price (1Y)", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)

def growth_line_chart(ticker, data, ticker2=None, data2=None):
    # st.text(ticker )

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data.values, mode='lines+markers', name=data.name))


    fig.update_layout(title=f"{ticker} {data.name} Growth Over Time", xaxis_title="Year", yaxis_title="Percent Change", yaxis_tickformat=".2%")

    st.plotly_chart(fig, use_container_width=True)

    return fig
