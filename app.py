import streamlit as st
import yfinance as yf
import pandas as pd
# from utils import ticker_exists
# from financial_analyzer import Analyzer

from data.fetcher import (
    get_stock_object,
    get_price_history,
    get_company_info,
    get_dividends,
    get_earnings,
    get_financial_statements,
    get_peers
)

from analysis.ratios import (
    calculate_profit_margin,
    calculate_ROE,
    calculate_DE_ratio,
    calculate_current_ratio,
    calculate_quick_ratio,
    calculate_interest_coverage
)

from visuals.layout import (safe_metric)


def main():

    st.sidebar.title("📊 Financial Analyzer")

    st.sidebar.header("Compare Companies")
    ticker1 = st.sidebar.text_input("Primary Ticker", value="AAPL")
    ticker2 = st.sidebar.text_input("Compare With (Optional)")

    display = st.sidebar.radio("Display:", ['Core Financial Ratios', 'Growth Metrics',
                               'Cash Flow & Efficiency', 'Valuation Metrics', 'Stock Performance Metrics'])

    if ticker1:

        financials, balance_sheet, cash_flows = get_financial_statements(ticker1)
        if ticker2:
            financials2, balance_sheet2, cash_flows2 = get_financial_statements(ticker2)

        if display == "Core Financial Ratios":

            st.header("📌 Core Financial Ratios")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader(ticker1)
                st.markdown("<hr style='margin-top: -10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

                safe_metric('Profit Margin',calculate_profit_margin(financials), "{:.2%}")
                safe_metric('ROE', calculate_ROE(financials, balance_sheet), "{:.2%}")
                safe_metric('Debt-to-Equity', calculate_DE_ratio(balance_sheet), "{:.2%}")
                safe_metric('Current Ratio', calculate_current_ratio(balance_sheet), "{:.2%}")
                safe_metric('Quick Ratio', calculate_quick_ratio(balance_sheet), "{:.2%}")

            if ticker2:
                with col2:
                    st.subheader(ticker2)
                    st.markdown("<hr style='margin-top: -10px; margin-bottom: 20px;'>", unsafe_allow_html=True)
                    safe_metric('Profit Margin',calculate_profit_margin(financials2), "{:.2%}")
                    safe_metric('ROE', calculate_ROE(financials2, balance_sheet2), "{:.2%}")
                    safe_metric('Debt-to-Equity', calculate_DE_ratio(balance_sheet2), "{:.2%}")
                    safe_metric('Current Ratio', calculate_current_ratio(balance_sheet2), "{:.2%}")
                    safe_metric('Quick Ratio', calculate_quick_ratio(balance_sheet2), "{:.2%}")


        elif display == "Growth Metrics":
            st.text("Revenue Growth Rate, Net Income Growth Rate, EPS Growth Rate, Free Cash Flow Growth")
            

        elif display == "Cash Flow & Efficiency":
            st.text("Free Cash Flow, FCF Margin, Operating Margin, Asset Turnover")

        elif display == "Valuation Metrics":
            st.text("Price-to-Earnings, Forward PE, Price-to-Book, EV/EBITA, PEG Ratio")

        elif display == "Stock Performance Metrics":
            st.text("Volatility, Sharpe Ratio, Drawdown Analysis, Moving Averages, RSI / MACD ?")
    else:
        st.warning("Please enter primary ticker symbol")


main()
