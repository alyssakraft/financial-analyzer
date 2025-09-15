import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

from utils.constants import GROWTH_LABELS, VALUATION_LABELS, CF_LABELS, STOCK_LABELS

from data.fetcher import (get_company_name, get_price_history, get_financial_statements)

from analysis.ratios import calculate_ratios
from analysis.valuation import get_valuation_metrics
from visuals.charts import (plot_stocks, growth_line_chart)

from analysis.performance import ( calculate_efficiency_metrics, calculate_stock_metrics)

from analysis.growth import(get_metric_series, calculate_growth_series)
from visuals.layout import (col_display_metric, display_MetricData)
from analysis.insights import (ratio_insights, valuation_insights)
from utils.formatter import format_large_number


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
        ticker1_name = get_company_name(ticker1)
        financials, balance_sheet, cash_flows = get_financial_statements(ticker1)
        hist1 = get_price_history(ticker1)

        # if comparing, get ticker2 info
        if ticker2:
            ticker2_name = get_company_name(ticker2)
            financials2, balance_sheet2, cash_flows2 = get_financial_statements(ticker2)
            hist2 = get_price_history(ticker2)
            tickers = [ticker1_name, ticker2_name]


        # -----------------------------------#
        #   Core Financial Ratios -- DONE
        # -----------------------------------#
        if display == "Core Financial Ratios":
            st.header("📌 Core Financial Ratios")

            ratio_metrics1 = calculate_ratios(financials, balance_sheet)

            if ticker2:
                ratio_metrics2 = calculate_ratios(financials2, balance_sheet2)
                col_display_metric(tickers, ratio_metrics1, ratio_metrics2)
                
            else:
                insights = ratio_insights(ratio_metrics1)
                display_MetricData(ticker1_name, ratio_metrics1, insights)
                # display_metric(ticker1_name, ratio_metrics1, insights)

                
        # -----------------------------------#
        #  Growth Metrics -- ADD INSIGHTS
        # -----------------------------------#
        elif display == "Growth Metrics":
            st.title("📈 Growth Metrics")

            tabs = st.tabs(GROWTH_LABELS)
            for tab, label in zip(tabs, GROWTH_LABELS):
                with tab:
                    series1 = get_metric_series(financials, cash_flows, label)
                    if ticker2:
                        series2 = get_metric_series(financials2, cash_flows2, label)
                        df = pd.concat([series1, series2], axis=1).dropna()
                        df.columns = [ticker1_name, ticker2_name]
                    else:
                        df = series1.to_frame().dropna()

                    if series1 is not None:
                        growth = calculate_growth_series(series1)
                        growth.name = label
                        growth_line_chart(ticker1, growth)

                        if not label == "Diluted EPS":
                            df = df.style.format(format_large_number)

                        st.text(f"{label} Over Time")
                        st.dataframe(df)
                    else:
                        st.caption(f"⚠️ {label} data not available.")


        # -----------------------------------#
        #   Cash Flow & Efficiency -- MAKE MORE COMPREHENSIVE
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
                    a.name = ticker1_name
                    b.name = ticker2_name

                    st.subheader(l)
                    st.dataframe(pd.concat([a,b], axis=1).dropna())

                    # insights
            else:
                # insights
                for e, l in zip(efficiency1, CF_LABELS):
                    st.subheader(l)

                    e.name = ticker1
                    st.dataframe(e)


        # -----------------------------------#
        #   Valuation Metrics -- DONE
        # -----------------------------------#
        elif display == "Valuation Metrics":
            st.header("💰 Valuation Metrics")

            # get valuation calculations as series, good for scalability
            valuation_series1 = get_valuation_metrics(ticker1)

            if ticker2:
                valuation_series2 = get_valuation_metrics(ticker2)
                col_display_metric(tickers, valuation_series1, valuation_series2)
            else:
                insights = valuation_insights(valuation_series1)
                display_MetricData(ticker1_name, valuation_series1, insights)
                

        # -----------------------------------#
        #   Stock Metrics -- CHANGE CUMULATIVE RETURN TO GRAPH
        # -----------------------------------#
        elif display == "Stock Performance Metrics":
            # plot historical stock prices
            st.title("📉 Stock Performance Metrics")

            stock_series1 = calculate_stock_metrics(hist1)

            if ticker2:
                plot_stocks(ticker1, ticker2)
                stock_series2 = calculate_stock_metrics(hist2)
                col_display_metric(tickers, stock_series1, stock_series2)
            else:
                plot_stocks(ticker1)
                display_MetricData(ticker1_name, stock_series1)

            # display cumilative return graph
            

    else:
        st.warning("Please enter primary ticker symbol")


main()
