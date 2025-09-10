# volatility, drawdowns, moving averages
# analysis/performance.py

import numpy as np
import pandas as pd
from data.fetcher import get_value_by_label
import streamlit as st

def calculate_fcf(cashflow):
    """Free Cash Flow = Operating Cash Flow − Capital Expenditures"""

    try:
        # operating_cf = cashflow.loc["Total Cash From Operating Activities"]
        operating_cf = get_value_by_label(cashflow, ["Total Cash From Operating Activities", "Operating Cash Flow"])
        # capex = cashflow.loc["Capital Expenditures"]
        capex = get_value_by_label(cashflow, ["Capital Expenditures", "Purchase Of PPE"])
        # st.table(operating_cf)
        # st.table(capex)
        fcf = operating_cf - capex
        fcf.index = pd.to_datetime(fcf.index).year
        return fcf.sort_index().dropna()
    except KeyError:
        return None


def calculate_fcf_margin(cashflow, financials):
    """FCF Margin = Free Cash Flow / Revenue"""
    fcf = calculate_fcf(cashflow)
    try:
        revenue = financials.loc["Total Revenue"]
        margin = fcf / revenue
        return margin.dropna()
    except (KeyError, TypeError):
        return None


def calculate_operating_margin(financials):
    """Operating Margin = Operating Income / Revenue"""
    try:
        operating_income = financials.loc["Operating Income"]
        revenue = financials.loc["Total Revenue"]
        margin = operating_income / revenue
        return margin.dropna()
    except KeyError:
        return None
    

def calculate_asset_turnover(financials, balance_sheet):
    """Asset Turnover = Revenue / Total Assets"""
    try:
        revenue = financials.loc["Total Revenue"]
        assets = balance_sheet.loc["Total Assets"]
        turnover = revenue / assets
        return turnover.dropna()
    except KeyError:
        return None


def calculate_interest_coverage(financials):
    """Interest Coverage = EBIT / Interest Expense"""
    try:
        ebit = financials.loc["EBIT"]
        interest = financials.loc["Interest Expense"]
        coverage = ebit / interest
        return coverage.dropna()
    except KeyError:
        return None


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
        "Volatility": volatility,
        "Sharpe Ratio": sharpe_ratio,
        "Max Drawdown": max_drawdown,
        "Cumulative Return": cumulative_return
    }
