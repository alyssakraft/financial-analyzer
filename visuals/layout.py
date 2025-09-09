# streamlit layout helps (columns, tabs, etc.)

import streamlit as st

def safe_metric(label, value, format_str="{:.2f}", suffix=""):
    """
    Displays a Streamlit metric if value is valid; otherwise shows a caption.
    """
    if value is not None:
        st.metric(label, format_str.format(value) + suffix)
    else:
        st.text("Debt-to-Equity")
        st.caption(f"⚠️ {label} not available.")
