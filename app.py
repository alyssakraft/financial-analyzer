import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

from utils.constants import RATIO_LABELS, GROWTH_LABELS, VALUATION_LABELS, CF_LABELS, STOCK_LABELS

from data.fetcher import (get_price_history, get_financial_statements)

from analysis.ratios import calculate_ratios
from analysis.valuation import get_valuation_metrics
from visuals.charts import (plot_stocks, growth_line_chart)

from analysis.performance import ( calculate_efficiency_metrics, calculate_fcf, calculate_stock_metrics)

from analysis.growth import(get_metric_series, calculate_growth_series)
from visuals.layout import ( display_metric, col_display_metric)


def main():

    # create sidebar for user inputs, display results on page
    st.sidebar.title("📊 Financial Analyzer")

    # get primary and compare tickers from user
    st.sidebar.header("Compare Companies")
    ticker1 = st.sidebar.text_input("Primary Ticker", value="AAPL")
    ticker2 = st.sidebar.text_input("Compare With (Optional)")

    # show calculation options
    display = st.sidebar.radio("Display:", ['Core Financial Ratios', 'Growth Metrics',
                               'Cash Flow & Efficiency', 'Valuation Metrics', 'Stock Performance Metrics'])

    if ticker1:

        # get info from ticker needed for calculations
        financials, balance_sheet, cash_flows = get_financial_statements(ticker1)
        hist1 = get_price_history(ticker1)

        # if comparing, get ticker2 info
        if ticker2:
            financials2, balance_sheet2, cash_flows2 = get_financial_statements(ticker2)
            hist2 = get_price_history(ticker2)
            tickers = [ticker1, ticker2]


        # -----------------------------------#
        #   Core Financial Ratios
        # -----------------------------------#
        if display == "Core Financial Ratios":
            st.header("📌 Core Financial Ratios")

            ratio_metrics1 = calculate_ratios(financials, balance_sheet)
            insights = {
                "Profit Margin": "[Insight for PM]"
            }

            if ticker2:
                ratio_metrics2 = calculate_ratios(financials2, balance_sheet2)
                col_display_metric(tickers, ratio_metrics1, ratio_metrics2)
                
            else:
                display_metric(ticker1, ratio_metrics1, insights)

                
        # -----------------------------------#
        #  Growth Metrics
        # -----------------------------------#
        elif display == "Growth Metrics":
            st.title("📈 Growth Metrics")

            tabs = st.tabs(GROWTH_LABELS)

            for tab, label in zip(tabs, GROWTH_LABELS):
                with tab:
                    if label == "Free Cash Flow":
                        series1 = calculate_fcf(cash_flows)

                    else: 
                        series1 = get_metric_series(financials, label)

                    if series1 is not None:
                        growth = calculate_growth_series(series1)
                        st.plotly_chart(growth_line_chart(label, growth), use_container_width=True)

                        st.table(growth)
                    else:
                        st.caption(f"⚠️ {label} data not available.")


        # -----------------------------------#
        #   Cash Flow & Efficiency
        # -----------------------------------#
        elif display == "Cash Flow & Efficiency":
            st.title("⚙️ Efficiency Metrics")

            efficiency_metrics1 = calculate_efficiency_metrics(cash_flows, financials, balance_sheet)
            efficiency1 = [efficiency_metrics1[e] for e in efficiency_metrics1 if e in CF_LABELS]
            
            tables = []
            if ticker2:
                efficiency_metrics2 = calculate_efficiency_metrics(cash_flows2, financials2, balance_sheet2)
                efficiency2 = [efficiency_metrics2[e] for e in efficiency_metrics2 if e in CF_LABELS]

                tables = []
                for a, b, l in zip(efficiency1, efficiency2, CF_LABELS):
                    a.name = ticker1
                    b.name = ticker2 

                    st.subheader(l)
                    st.dataframe(pd.concat([a,b], axis=1).dropna())

                    # insights
            else:
                # insights
                for e, l in zip(efficiency1, CF_LABELS):
                    e.name = l
                    st.dataframe(e)


        # -----------------------------------#
        #   Valuation Metrics
        # -----------------------------------#
        elif display == "Valuation Metrics":
            st.header("💰 Valuation Metrics")

            # get valuation calculations as series, good for scalability
            valuation_series1 = get_valuation_metrics(ticker1)

            if ticker2:
                valuation_series2 = get_valuation_metrics(ticker2)
                col_display_metric(tickers, valuation_series1, valuation_series2)
            else:
                display_metric(ticker1, valuation_series1)

        # -----------------------------------#
        #   Stock Metrics
        # -----------------------------------#
        elif display == "Stock Performance Metrics":
            # plot historical stock prices
            st.title("📉 Stock Performance Metrics")

            plot_stocks(ticker1)
            
            stock_series1 = calculate_stock_metrics(hist1)

            if ticker2:
                stock_series2 = calculate_stock_metrics(hist2)
                col_display_metric(tickers, stock_series1, stock_series2)
            else:
                display_metric(ticker1, stock_series1)
            

    else:
        st.warning("Please enter primary ticker symbol")


main()
