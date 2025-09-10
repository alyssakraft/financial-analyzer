# streamlit layout helps (columns, tabs, etc.)

import streamlit as st
import pandas as pd
from utils.constants import RATIO_LABELS, GROWTH_LABELS, VALUATION_LABELS, CF_LABELS, STOCK_LABELS


def safe_metric(label, value, format_str="{:.2f}", suffix=""):
    """
    Displays a Streamlit metric if value is valid, otherwise shows a caption.
    """
    if value is not None:
        st.metric(label, format_str.format(value) + suffix)
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

def col_display(col, li, text, labels=None):
    with col:
        st.subheader(li.pop(0))
        st.markdown("<hr style='margin-top: -10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        if labels:
            for l, m in zip(labels, li):
                # st.text(f"{l} = {m}")
                safe_metric(l, m)

                st.text(text)


def col_display_compare(left, right, l_labels, r_labels=None):

    col1, col2 = st.columns(2, width="stretch")

    col_display(col1, left, None, l_labels)
    col_display(col2, right, None, r_labels)

def display_insights(data, insights, labels):
    for d, i, l in zip(data, insights, labels):
        safe_metric(l, d)
        st.text(i)
        st.markdown("<hr style='margin-top: -10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

