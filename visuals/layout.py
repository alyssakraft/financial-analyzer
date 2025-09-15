# streamlit layout helps (columns, tabs, etc.)

import streamlit as st
import pandas as pd
from utils.constants import RATIO_LABELS, GROWTH_LABELS, VALUATION_LABELS, CF_LABELS, STOCK_LABELS
from data.metric_data import MetricData


def safe_metricData(m: MetricData):
    if m.value is not None and m.delta is None:
        st.metric(m.name, m.formatted_value())
    elif m.delta is not None:
        st.metric(m.name, m.formatted_value(), delta=f"{m.delta:.2f}")
    else:
        st.text(m.name)
        st.caption(f"⚠️ {m.name} not available.")


def display_MetricData(label, data: dict, insights=None):
    st.subheader(label)
    st.markdown("<hr style='margin-top: -10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

    for name, val in data.items():
        if isinstance(val, MetricData):
            safe_metricData(val)
        else:
            safe_metric(name, val)

        
        if insights is not None and name in insights:
                st.text(insights[name])
        st.markdown("<hr style='margin-top: -10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

    return


def safe_metric(label, value, format_str="{:.2f}", suffix="", delta=None):
    """
    Displays a Streamlit metric if value is valid, otherwise shows a caption.
    """
    if value is not None and delta is None:
        st.metric(label, format_str.format(value) + suffix)
    elif delta is not None:
        st.metric(label, format_str.format(value) + suffix, delta=f"{delta:.2f}")
    else:
        st.text(label)
        st.caption(f"⚠️ {label} not available.")

def safe_df(label, df):
    """
    Displays a Streamlit datafram if value is valid, otherwise shows a caption.
    """

    if not df.empty:
        df.name = label
        st.dataframe(df)
    else:
        st.caption(f"⚠️ {label} not available.")


def col_display_metric(tickers, data1, data2):
    col1, col2 = st.columns(2)
    with col1: 
        display_MetricData(tickers[0], data1)
    with col2:
        display_MetricData(tickers[1], data2)

