# volatility, drawdowns, moving averages
# analysis/performance.py

import numpy as np
import pandas as pd
from data.fetcher import get_value_by_label
import streamlit as st
from data.metric_data import MetricData
from utils.constants import VOLATILITY, SHARPE_RATIO, MAX_DRAWDOWN, CUMULATIVE_RETURN

def calculate_fcf(cash_flows):
    """Free Cash Flow = Operating Cash Flow − Capital Expenditures"""

    try:
        # operating_cf = cash_flows.loc["Total Cash From Operating Activities"]
        operating_cf = get_value_by_label(cash_flows, ["Total Cash From Operating Activities", "Operating Cash Flow"])
        # capex = cash_flows.loc["Capital Expenditures"]
        capex = get_value_by_label(cash_flows, ["Capital Expenditures", "Purchase Of PPE"])
        # st.table(operating_cf)
        # st.table(capex)
        fcf = operating_cf - capex
        fcf.index = pd.to_datetime(fcf.index).year
        return fcf.sort_index().dropna()
    except KeyError:
        return None


def calculate_fcf_margin(cash_flows, financials):
    """FCF Margin = Free Cash Flow / Revenue"""
    fcf = calculate_fcf(cash_flows)
    try:
        revenue = get_value_by_label(financials, ["Total Revenue"])
        revenue.index = revenue.index.year
        # st.table(revenue)
        # st.table(fcf)
        margin = fcf / revenue
        return margin.sort_index().dropna()
    except (KeyError, TypeError):
        return None


def calculate_operating_margin(financials):
    """Operating Margin = Operating Income / Revenue"""
    try:
        operating_income = financials.loc["Operating Income"]
        revenue = financials.loc["Total Revenue"]
        margin = operating_income / revenue
        margin.index = margin.index.year
        return margin.sort_index().dropna()
    except KeyError:
        return None
    

def calculate_asset_turnover(financials, balance_sheet):
    """Asset Turnover = Revenue / Total Assets"""
    try:
        revenue = financials.loc["Total Revenue"]
        assets = balance_sheet.loc["Total Assets"]
        turnover = revenue / assets
        turnover.index = turnover.index.year
        return turnover.sort_index().dropna()
    except KeyError:
        return None


def calculate_interest_coverage(financials):
    """Interest Coverage = EBIT / Interest Expense"""
    try:
        ebit = financials.loc["EBIT"]
        interest = financials.loc["Interest Expense"]
        coverage = ebit / interest
        coverage.index = coverage.index.year
        return coverage.sort_index().dropna()
    except KeyError:
        return None
    
def calculate_efficiency_metrics(cash_flows, financials, balance_sheet):
    """Calculate efficiency metrics and return as a series"""
    series = {
        "Free Cash Flows": calculate_fcf(cash_flows),
        "FCF Margin": calculate_fcf_margin(cash_flows, financials),
        "Operating Margin": calculate_operating_margin(financials),
        "Asset Turnover": calculate_asset_turnover(financials, balance_sheet),
        "Interest Coverage": calculate_interest_coverage(financials)
    }

    return series
    pass


def calculate_stock_metrics(price_df, risk_free_rate=0.015):
    price_df['Return'] = price_df['Close'].pct_change()
    daily_returns = price_df['Return'].dropna()

    volatility = np.std(daily_returns)
    mean_return = np.mean(daily_returns)
    sharpe_ratio = (mean_return - risk_free_rate / 252) / volatility if volatility else None

    cumulative_return = (price_df['Close'].iloc[-1] / price_df['Close'].iloc[0]) - 1

    rolling_max = price_df['Close'].cummax()
    drawdown = (price_df['Close'] - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    return {
        VOLATILITY: MetricData(VOLATILITY, volatility, fmt="{:.2%}"),
        SHARPE_RATIO: MetricData(SHARPE_RATIO, sharpe_ratio),
        MAX_DRAWDOWN: MetricData(MAX_DRAWDOWN, max_drawdown, fmt="{:.2%}"),
        "Cumulative Return": cumulative_return
    }
