import pandas as pd
import streamlit as st
from data.fetcher import get_value_by_label

# PE, PB, EV/EBITDA, etc.


def calculate_profit_margin(financials: pd.DataFrame) -> float:
    """Net Income / Revenue"""
    try:
        # st.dataframe(get_row_safe(financials, 'Total Revenue'))
        # st.dataframe(get_row_safe(financials, 'Net Income'))

        revenue = get_value_by_label(financials, ['Total Revenue', 'Revenue'])[0]
        net_income = get_value_by_label(financials, ['Net Income'])[0]

        return net_income / revenue
    except (KeyError, IndexError, TypeError):
        return None


def calculate_ROE(financials: pd.DataFrame, balance_sheet: pd.DataFrame) -> float:
    """Net Income / Shareholder Equity"""
    try:
        net_income = get_value_by_label(financials, ['Net Income'])[0]
        equity = get_value_by_label(balance_sheet, ['Stockholders Equity', 'Total Stockholders Equity'])[0]

        return net_income / equity
    except (KeyError, IndexError, TypeError):
        return None


def calculate_DE_ratio(balance_sheet: pd.DataFrame) -> float:
    """Total Liabilities / Shareholder Equity"""
    try:
        liabilities = get_value_by_label(balance_sheet, ['Total Liabilities'])[0]

        if liabilities == None:
            current_liabilities = get_value_by_label(balance_sheet, ['Current Liabilities'])
            non_current_liabilities = get_value_by_label(balance_sheet, ['Total Non Current Liabilities Net Minority Interest'])
            if current_liabilities is None and non_current_liabilities is None:
                return None

            liabilities = non_current_liabilities + current_liabilities

        equity = get_value_by_label(balance_sheet, ['Stockholders Equity', 'Total Stockholders Equity'])[0]
        return liabilities / equity
    
    except (KeyError, IndexError, TypeError):
        # st.warning("Could not find Total Liabilities for this ticker:")
        return None


def calculate_current_ratio(balance_sheet: pd.DataFrame) -> float:
    """Current Assets / Current Liabilities"""
    try:
        current_assets = get_value_by_label(balance_sheet, ['Total Current Assets', 'Current Assets'])[0]
        current_liabilities = get_value_by_label(balance_sheet, ['Total Current Liabilities', 'Current Liabilities'])[0]

        return current_assets / current_liabilities
    except (KeyError, IndexError, TypeError):
        return None


def calculate_quick_ratio(balance_sheet: pd.DataFrame) -> float:
    """(Current Assets − Inventory) / Current Liabilities"""
    try:
        current_assets = get_value_by_label(balance_sheet, ['Total Current Assets', 'Current Assets'])[0]
        inventory = get_value_by_label(balance_sheet, ['Inventory'])[0]
        current_liabilities = get_value_by_label(balance_sheet, ['Total Current Liabilites', 'Current Liabilities'])[0]

        return (current_assets - inventory) / current_liabilities
    except (KeyError, IndexError, TypeError):
        return None


def calculate_interest_coverage(financials: pd.DataFrame) -> float:
    """EBIT / Interest Expense"""
    try:
        ebit = get_value_by_label(financials, ['EBIT'])[0]
        interest = get_value_by_label(financials, ['Interest Expense'])[0]

        return ebit / interest
    except (KeyError, IndexError, TypeError):
        return None
