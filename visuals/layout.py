# streamlit layout helps (columns, tabs, etc.)

import streamlit as st
import pandas as pd
from utils.constants import RATIO_LABELS, GROWTH_LABELS, VALUATION_LABELS, CF_LABELS, STOCK_LABELS


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

def safe_df_combined(label, df1, df2):
    if not df1.empty and not df2.empty:
        combined = pd.concat([df1, df2], axis=1)
        combined.name = label
        st.dataframe(combined)
    # elif df2.empty:
    else:
        st.caption(f"⚠️ {label} not available.")


def is_tuple(d):
    return all(isinstance(v, tuple) for v in d.values())


def display_metric(label, data: dict, insights=None):
    st.subheader(label)
    st.markdown("<hr style='margin-top: -10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

    if is_tuple(data):
        for d, (val, delta) in data.items():
            safe_metric(d, val, delta=delta)
            if insights is not None and d in insights:
                st.text(insights[d])
            st.markdown("<hr style='margin-top: -10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

    else:
        for d, val in data.items():
            safe_metric(d, val)



def col_display_metric(tickers, data1, data2):
    col1, col2 = st.columns(len(tickers))
    with col1: 
        display_metric(tickers[0], data1)
    with col2:
        display_metric(tickers[1], data2)
