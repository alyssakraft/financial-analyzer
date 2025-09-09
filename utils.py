import yfinance as yf
import streamlit as st


def ticker_exists(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        # Try to fetch some basic info
        info = ticker.info
        # If 'shortName' exists, ticker is valid
        if info and 'shortName' in info:
            return True
        else:
            st.warning("Invalid ticker, please try again")
            return False
    except Exception as e:
        # Any error (network issue, invalid ticker, etc.) will be caught here
        st.warning(f"Error checking ticker {ticker_symbol}: {e}")
        return False
