import streamlit as st
import yfinance as yf
from utils import ticker_exists
import pandas as pd
from financial_analyzer import Analyzer


def main():
    st.title("📊 Financial Analyzer")

    ticker_symbol = st.text_input(
        "Enter ticker symbol:", key="main_ticker").upper().strip()

    options = st.multiselect(
        "Select the data you want to view:",
        ["Revenue", "Net Income", "Financial Ratios", "Compare with Another Company"]
    )

    if "Compare with Another Company" in options:
        compare_input = st.text_input(
            "Enter another ticker to compare:", key="compare_symbol").upper().strip()

    if st.button("Analyze") and ticker_exists(ticker_symbol):

        company = Analyzer(ticker_symbol)
        st.header(f"Company: {company.ticker.info.get('shortName', 'N/A')}")

        if "Revenue" in options and company.revenue is not None:
            company.plot_financials({"Revenue": company.revenue})

        if "Net Income" in options and company.net_income is not None:
            company.plot_financials({"Net Income": company.net_income})

        if "Financial Ratios" in options and company.ratios is not None:
            st.subheader(f"{ticker_symbol} Financial Ratios")
            st.dataframe(company.ratios)

        if "Compare with Another Company" in options:

            if compare_input:
                other_company = Analyzer(compare_input)
                if other_company.ratios is not None:
                    st.subheader(f"Comparing {ticker_symbol} with {compare_input}")
                # for var in ['PM', 'ROE', 'D/E']:
                #     company.compare_ratios(other_company, var)
                    company.compare_ratios(other_company)
      
            else:
                st.warning("Please enter second ticker symbol")


main()
