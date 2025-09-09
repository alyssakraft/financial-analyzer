import streamlit as st
import yfinance as yf
from utils import ticker_exists
import pandas as pd
from financial_analyzer import Analyzer


st.title("📊 Financial Analyzer")


def main():
    ticker_symbol = st.text_input(
        "Enter ticker symbol:", key="main_ticker").upper().strip()

    a_type = st.radio("Select Analysis Type", ['Automatic', 'Custom'])
    # custom = st.radio("Custom")

    st.text("Select Financial Calculations")
    if a_type == 'Automatic':
        stock_summary = st.checkbox("Stock Summary")
        financial_models = st.checkbox("Financial Models")
        financial_ratios = st.checkbox("Financial Ratios")
    else:
        options = st.multiselect(
            "Select the data you want to view:",
            ["Model Stocks", "Price-to-Earnings (PE)", "Earnings Per Share (EPS)", "Dividend Yield and Payout Ratio",
             "Beta", "Model Revenue", "Model Net Income", "Financial Ratios", "Compare Financial Ratios with Another Company"]
        )

    # if user entered a valid ticker
    if st.button("Analyze") and ticker_exists(ticker_symbol):

        company = Analyzer(ticker_symbol)
        st.header(f"Company: {company.ticker.info.get('shortName', 'N/A')}")


main()
