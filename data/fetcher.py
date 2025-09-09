import yfinance as yf
import pandas as pd
# remove after testing
import streamlit as st


def get_stock_object(ticker: str):
    """return yfinance ticker"""
    return yf.Ticker(ticker)


def get_price_history(ticker: str, period="1y", interval="1d"):
    """fetch historical price data"""
    stock = get_stock_object(ticker)
    return stock.history(period=period, interval=interval)


def get_company_info(ticker: str):
    """fetch general company info (e.g., market cap, PE ratio)."""
    stock = get_stock_object(ticker)
    return stock.info


def get_financial_statements(ticker: str):
    """returns financials, balance sheet, and cashflow as DataFrames."""
    stock = get_stock_object(ticker)
    return stock.financials, stock.balance_sheet, stock.cashflow


def get_earnings(ticker: str):
    """Fetch quarterly earnings data."""
    stock = get_stock_object(ticker)
    return stock.earnings, stock.quarterly_earnings


def get_dividends(ticker: str):
    """Fetch dividend history."""
    stock = get_stock_object(ticker)
    return stock.dividends


def get_peers(ticker: str):
    """Returns a list of peer companies if available."""
    stock = get_stock_object(ticker)
    # Placeholder—yfinance doesn't always expose peers
    return stock.info.get("companyOfficers", [])


def get_value_by_label(df, possible_labels):
    """
    Searches for the first matching label in a DataFrame index.
    Returns the value from the most recent column.
    """
    # st.dataframe(df)
    # st.dataframe(possible_labels)
    for label in possible_labels:
        if label in df.index:
            return df.loc[label]  # Most recent year
    return None  # Graceful fallback
