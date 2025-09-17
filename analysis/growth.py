# revenue, net income, EPS growth

import pandas as pd
import streamlit as st
from analysis.performance import calculate_fcf

def calculate_growth_series(series):
    """
    Calculates year-over-year growth rates from a time series.
    Returns a Series of growth percentages.
    """
    return series.pct_change().dropna()

def get_metric_series(financials, cash_flows, label):
    """
    Extracts a time series for a given label from the financials DataFrame.
    Returns a Series indexed by year.
    """
    if label not in financials.index:
        if label == "Free Cash Flows":
            series = calculate_fcf(cash_flows)
        else:
            return None
    else:
        series = financials.loc[label]
    # Ensure index is datetime or year
        if not isinstance(series.index[0], (int, float)):
            # st.table(series)
            series.index = pd.to_datetime(series.index).year
        
    return series.sort_index()

