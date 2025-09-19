"""
data/fetcher.py

Handles data fetching from yfinance.
"""

import yfinance as yf

def ticker_exists(ticker):
    """check if ticker exists in yfinance."""

    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return info is not None and info.get("regularMarketPrice") is not None
    except Exception:
        return False

def get_stock_object(ticker: str):
    """return yfinance ticker"""
    return yf.Ticker(ticker)

def get_company_name(ticker: str):
    """fetch company name from ticker"""
    stock = get_stock_object(ticker)
    return stock.info.get("shortName", ticker)


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
    for label in possible_labels:
        if label in df.index:
            return df.loc[label]  # Most recent year
    return None  # Graceful fallback
