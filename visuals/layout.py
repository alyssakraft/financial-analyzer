"""
visuals/layout.py

Provides layout and display utilities for Streamlit.
"""

import streamlit as st
from data.metric_data import MetricData


def get_page_header(title, subtitle=None):
    """
    Displays a page header with an optional subtitle in Streamlit.
    """
    # markdown for title with large font and bold weight
    st.markdown(f"<p style='font-size: 2.75rem; font-weight: 700; margin: 0px;'>{title}</p>", unsafe_allow_html=True)

    # if subtitle is provided, display it with smaller font and lighter color
    if subtitle:
        st.markdown(f"<h1 style='font-size:0.875rem; font-weight: 450; color: #888888; margin-top: -1.5em;'>{subtitle}</h1>", unsafe_allow_html=True)

    # horizontal rules for visual separation    
    st.markdown("<hr style='margin-top: -10px; margin-bottom: 5px; border: 5px solid #212D41'>", unsafe_allow_html=True)
    st.markdown("<hr style='margin-top: -10px; margin-bottom: 5px; border: 5px solid #181C24'>", unsafe_allow_html=True)
    st.markdown("<hr style='margin-top: -10px; margin-bottom: 40px; border: 5px solid #11141A'>", unsafe_allow_html=True)
    

def safe_metricData(m: MetricData, is_second=False):
    """
    Displays a Streamlit metric if MetricData is valid, otherwise shows a caption.
    """
    if is_second:
        label = ""  # hide name for second column to reduce clutter
    else:
        label = m.name

    # display metric based on available data
    if m.value is not None and m.delta is None:
        st.metric(label, m.formatted_value())
    elif m.delta is not None:
        st.metric(label, m.formatted_value(), delta=f"{m.delta:.2f}")
    else:
        st.text(label)
        st.caption(f"⚠️ {label} not available.")


def display_MetricData(label, data: dict, insights=None, is_second=False):
    """
    Displays a set of metrics in Streamlit with optional insights.
    """

    # display section header
    st.subheader(label)
    st.markdown(f"<hr style='margin-top: -5px; margin-bottom: 20px; border: 2px solid #181C24;'>", unsafe_allow_html=True)

    # display each metric and its insight if available
    for name, val in data.items():
        if val is not None:
            if isinstance(val, MetricData):
                safe_metricData(val, is_second=is_second)

            if insights is not None and name in insights:
                st.info(insights[name])
            st.markdown("<hr style='margin-top: 5px; margin-bottom: 5px; border: 1px solid #0F1116'>", unsafe_allow_html=True)


def col_display_metric(tickers, data1, data2):
    """
    Displays two sets of metric data side by side in Streamlit columns.
    """

    col1, col2 = st.columns(2)
    with col1: 
        display_MetricData(tickers[0], data1)
    with col2:
        display_MetricData(tickers[1], data2, is_second=True)


def col_display_insights(ticker1, data, insights, no_delta=True):
    """
    Displays a set of metrics with insights in Streamlit columns.
    """

    test_margin = 20
    col1, col2 = st.columns([2, 3])

    # adjust height and margins based on whether deltas are present
    if no_delta:
        height = "82px"
        insight_margins = "5px"
        md_margin_bottom = "35px"
    else:
        height = "97.5px"
        insight_margins = "10px"
        md_margin_bottom = "30px"

    # display headers
    with col1:
        st.subheader(ticker1)
        st.markdown(f"<hr style='margin-top: -5px; margin-bottom: {md_margin_bottom}; border: 2px solid #181C24;'>", unsafe_allow_html=True)
    with col2:
        st.subheader("Key Insights")
        st.markdown(f"<hr style='margin-top: -5px; margin-bottom: 20px; border: 2px solid #181C24;'>", unsafe_allow_html=True)

    # display metrics and insights side by side
    for name, val in data.items():
        if name is not None:
            with col1:
                safe_metricData(val)
                st.markdown("<hr style='margin-top: 5px; margin-bottom: 5px; border: 1px solid #0F1116;'>", unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                    <div style='
                        margin-bottom: {insight_margins};
                        margin-top: {insight_margins};
                        background-color: #212D41;
                        border-radius: 8px;
                        border: 3px solid #1A2333;
                        padding: 10px;
                        height: {height};
                        color: #D2EAE4;
                        overflow-y: auto;
                        font-size: 16px;
                        line-height: 1.4;
                        text-align: left;
                        display: flex;
                        align-items: center;
                    '>
                        <div>
                            <p style='margin: 0;'>{insights[name] if name in insights else "N/A"}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<hr style='margin-top: 5px; margin-bottom: 5px; border: 1px solid #0F1116;'>", unsafe_allow_html=True)

