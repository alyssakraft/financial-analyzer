# analysis/ratios.py
"""
analysis/ratios.py

Calculates key financial ratios from financial statements.
"""

import pandas as pd
import streamlit as st
from data.fetcher import get_value_by_label
from data.metric_data import MetricData
from utils.formatter import format_delta
from utils.constants import PM, ROE, DE, CR, QR

# store calculated ratios in cache for performance
@st.cache_data
def calculate_ratios(financials, balance_sheet):
    """Calculate all financial ratios and return as a series."""

    series = {
        PM: (calculate_profit_margin(financials)),
        ROE: calculate_ROE(financials, balance_sheet),
        DE: calculate_DE_ratio(balance_sheet),
        CR: calculate_current_ratio(balance_sheet),
        QR: calculate_quick_ratio(balance_sheet)
    }
    return series


def calculate_profit_margin(financials: pd.DataFrame):
    """Net Income / Revenue"""

    try:
        revenue = get_value_by_label(financials, ['Total Revenue', 'Revenue'])
        net_income = get_value_by_label(financials, ['Net Income'])

        curr = net_income[0] / revenue[0]
        prev = net_income[1] / revenue[1]

        return MetricData(PM, curr, format_delta(curr, prev, True), "{:.2%}")

    except (KeyError, IndexError, TypeError):
        return None


def calculate_ROE(financials: pd.DataFrame, balance_sheet: pd.DataFrame) -> float:
    """Net Income / Shareholder Equity"""

    try:
        net_income = get_value_by_label(financials, ['Net Income'])
        equity = get_value_by_label(balance_sheet, ['Stockholders Equity', 'Total Stockholders Equity'])

        curr = net_income[0] / equity[0]
        prev = net_income[1] / equity[1]

        return MetricData(ROE, curr, format_delta(curr, prev, True), "{:.2%}")

    except (KeyError, IndexError, TypeError):
        return MetricData(ROE, None)


def calculate_DE_ratio(balance_sheet: pd.DataFrame) -> float:
    """Total Liabilities / Shareholder Equity"""

    try:
        liabilities = get_value_by_label(balance_sheet, ['Total Liabilities'])

        if liabilities == None:
            current_liabilities = get_value_by_label(balance_sheet, ['Current Liabilities'])
            non_current_liabilities = get_value_by_label(balance_sheet, ['Total Non Current Liabilities Net Minority Interest'])
            if current_liabilities is None and non_current_liabilities is None:
                return None

            calculated_liab = non_current_liabilities + current_liabilities

        equity = get_value_by_label(balance_sheet, ['Stockholders Equity', 'Total Stockholders Equity'])

        curr = calculated_liab[0] / equity[0]
        prev = calculated_liab[1] / equity[1]

        return MetricData(DE, curr, format_delta(curr, prev))
    
    except (KeyError, IndexError):
        return MetricData(DE, None)


def calculate_current_ratio(balance_sheet: pd.DataFrame) -> float:
    """Current Assets / Current Liabilities"""

    try:
        current_assets = get_value_by_label(balance_sheet, ['Total Current Assets', 'Current Assets'])
        current_liabilities = get_value_by_label(balance_sheet, ['Total Current Liabilities', 'Current Liabilities'])

        curr = current_assets[0] / current_liabilities[0]
        prev = current_assets[1] / current_liabilities[1]

        return MetricData(CR, curr, format_delta(curr, prev))

    except (KeyError, IndexError, TypeError):
        return MetricData(CR, None)


def calculate_quick_ratio(balance_sheet: pd.DataFrame) -> float:
    """(Current Assets - Inventory) / Current Liabilities"""

    try:
        current_assets = get_value_by_label(balance_sheet, ['Total Current Assets', 'Current Assets'])
        inventory = get_value_by_label(balance_sheet, ['Inventory'])
        
        current_liabilities = get_value_by_label(balance_sheet, ['Total Current Liabilites', 'Current Liabilities'])

        curr = (current_assets[0] - inventory[0]) / current_liabilities[0]
        prev = (current_assets[1] - inventory[1]) / current_liabilities[1]

        return MetricData(QR, curr, format_delta(curr, prev))

    except (KeyError, IndexError, TypeError):
        return MetricData(QR, None)


def calculate_interest_coverage(financials: pd.DataFrame) -> float:
    """EBIT / Interest Expense"""
    
    try:
        ebit = get_value_by_label(financials, ['EBIT'])
        interest = get_value_by_label(financials, ['Interest Expense'])

        curr = ebit[0] / interest[0]
        prev = ebit[1] / interest[1]

        return MetricData("Interest Coverage", curr, format_delta(curr, prev))

    except (KeyError, IndexError, TypeError):
        return None
