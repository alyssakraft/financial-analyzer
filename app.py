import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

from data.fetcher import (
    get_price_history,
    get_financial_statements,
)

from analysis.ratios import (
    calculate_profit_margin,
    calculate_ROE,
    calculate_DE_ratio,
    calculate_current_ratio,
    calculate_quick_ratio,
)

from analysis.performance import (
    calculate_fcf,
    calculate_fcf_margin,
    calculate_operating_margin,
    calculate_asset_turnover,
    calculate_interest_coverage,
    calculate_stock_metrics
)

from analysis.valuation import (get_valuation_metrics)
from analysis.growth import(calculate_fcf1, get_metric_series, calculate_growth_series)
from visuals.layout import (safe_metric)
from visuals.charts import (plot_stocks, growth_line_chart)

GROWTH_LABELS = [
    "Total Revenue",
    "Net Income",
    "Diluted EPS",
    "Free Cash Flow"
]


def main():

    st.sidebar.title("📊 Financial Analyzer")

    st.sidebar.header("Compare Companies")
    ticker1 = st.sidebar.text_input("Primary Ticker", value="AAPL")
    ticker2 = st.sidebar.text_input("Compare With (Optional)")

    display = st.sidebar.radio("Display:", ['Core Financial Ratios', 'Growth Metrics',
                               'Cash Flow & Efficiency', 'Valuation Metrics', 'Stock Performance Metrics'])

    if ticker1:

        # core financial ratios
        financials, balance_sheet, cash_flows = get_financial_statements(ticker1)
        hist1 = get_price_history(ticker1)

        if ticker2:
            financials2, balance_sheet2, cash_flows2 = get_financial_statements(ticker2)
            hist2 = get_price_history(ticker2)

        # stock metrics
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
            # else
            # give insights to company1 metrics?


        elif display == "Growth Metrics":
            st.title("📈 Growth Metrics")

            # st.dataframe()

            tabs = st.tabs(GROWTH_LABELS)

            for tab, label in zip(tabs, GROWTH_LABELS):
                with tab:
                    if label == "Free Cash Flow":
                        series = calculate_fcf1(cash_flows)
                    else: series = get_metric_series(financials, label)

                    if series is not None:
                        growth = calculate_growth_series(series)
                        st.plotly_chart(growth_line_chart(label, growth), use_container_width=True)

                        st.table(growth)
                    else:
                        st.caption(f"⚠️ {label} data not available.")


        elif display == "Cash Flow & Efficiency":
            # st.text("Free Cash Flow, FCF Margin, Operating Margin, Asset Turnover")
            st.title("⚙️ Efficiency Metrics")

            st.dataframe(cash_flows)

            # safe_metric("Free Cash Flows", calculate_fcf(cash_flows))
            # safe_metric("FCF Margin", calculate_fcf_margin(cash_flows, financials))

            st.dataframe(calculate_fcf(cash_flows))
            # safe_metric("Operating Margin", calculate_operating_margin(financials))
            # safe_metric("Asset Turnover", calculate_asset_turnover(financials, balance_sheet))
            # safe_metric("Interest Coverage", calculate_interest_coverage(financials))


        elif display == "Valuation Metrics":
            # st.text("Price-to-Earnings, Forward PE, Price-to-Book, EV/EBITA, PEG Ratio")
            st.header("💰 Valuation Metrics")

            valuation = get_valuation_metrics(ticker1)

            col1, col2, col3 = st.columns(3)
            safe_metric("Trailing P/E", valuation["Trailing P/E"], "{:.2f}")
            safe_metric("Forward P/E", valuation["Forward P/E"], "{:.2f}")
            safe_metric("PEG Ratio", valuation["PEG Ratio"], "{:.2f}")
            safe_metric("Price-to-Book", valuation["Price-to-Book"], "{:.2f}")
            safe_metric("Market Cap", valuation["Market Cap"], "{:,.0f}", suffix=" USD")


        elif display == "Stock Performance Metrics":
            st.text("Volatility, Sharpe Ratio, Drawdown Analysis, Moving Averages, RSI / MACD ?")
            # plot historical prices
            st.title("📉 Stock Performance Metrics")

            plot_stocks(ticker1)
            
            metrics = calculate_stock_metrics(hist1)
            safe_metric("Volatility", metrics["Volatility"], "{:.2f}")
            safe_metric("Sharpe Ratio", metrics["Sharpe Ratio"], "{:.2f}")
            safe_metric("Max Drawdown", metrics["Max Drawdown"], "{:.2f}")
            safe_metric("Cumulative Return", metrics["Cumulative Return"], "{:.2f}")


            # fig = go.Figure()
            # fig.add_trace(go.Scatter(x=hist1.index, y=hist1['Close'], name=ticker1))
            # fig.update_layout(title=f"{ticker1} Closing Price (1Y)", xaxis_title="Date", yaxis_title="Price")
            # st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Please enter primary ticker symbol")


main()
