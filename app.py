"""
app.py

Main application file for the Financial Analyzer Streamlit app.
"""

import streamlit as st
import pandas as pd

from data.fetcher import (ticker_exists, get_company_name, get_price_history, get_financial_statements)
from utils.constants import GROWTH_LABELS, CF_LABELS, CF_BOUNDS

from analysis.ratios import calculate_ratios
from analysis.growth import(get_growth_metrics, calculate_growth_series)
from analysis.valuation import get_valuation_metrics
from visuals.charts import (plot_stocks, growth_line_chart)
from analysis.performance import (calculate_efficiency_metrics, calculate_stock_metrics)

from visuals.layout import (get_page_header, col_display_metric, display_MetricData, col_display_insights)
from analysis.insights import (ratio_insights, growth_insights, valuation_insights, efficiency_insights)
from utils.formatter import (format_large_number, highlight_df_bounds)

st.set_page_config(page_title="Financial Analyzer", page_icon="📊", layout="wide")


def main():
    # create sidebar for user inputs, display results on page
    st.sidebar.title("📊 Financial Analyzer")
    st.sidebar.markdown("<hr style='margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)

    # get primary and compare ticker_names from user
    st.sidebar.header("Compare Companies")
    ticker1 = st.sidebar.text_input("Primary Ticker").upper()
    ticker2 = st.sidebar.text_input("Compare With (Optional)").upper()

    # show analysis options in sidebar
    display = st.sidebar.radio("Display:", ['Core Financial Ratios', 'Growth Metrics',
                               'Valuation Metrics', 'Stock Performance Metrics', 'Cash Flow & Efficiency'])
    st.sidebar.markdown("<hr style='margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)


    if ticker_exists(ticker1):

        # get info from ticker needed for calculations
        ticker1_name = get_company_name(ticker1)
        financials, balance_sheet, cash_flows = get_financial_statements(ticker1)
        hist1 = get_price_history(ticker1)

        # if comparing with a valid ticker, get ticker2 info
        if ticker2 and ticker_exists(ticker2):
            ticker2_name = get_company_name(ticker2)
            financials2, balance_sheet2, cash_flows2 = get_financial_statements(ticker2)
            hist2 = get_price_history(ticker2)
            ticker_names = [ticker1_name, ticker2_name]

        elif ticker2:
            st.sidebar.error("⚠️ Invalid compare ticker symbol.")
            ticker2 = None


        # -----------------------------------
        #   Core Financial Ratios
        # -----------------------------------
        if display == "Core Financial Ratios":
            #Displays core financial ratios and insights or compares ratios between two companies.

            get_page_header("Core Financial Ratios", "Key financial ratios to assess company performance.")

            ratio_metrics1 = calculate_ratios(financials, balance_sheet)

            if ticker2:
                ratio_metrics2 = calculate_ratios(financials2, balance_sheet2)
                col_display_metric(ticker_names, ratio_metrics1, ratio_metrics2)
                
            else:
                insights = ratio_insights(ratio_metrics1)
                col_display_insights(ticker1_name, ratio_metrics1, insights, False)

                
        # -----------------------------------
        #  Growth Metrics
        # -----------------------------------
        elif display == "Growth Metrics":
            # Displays growth metrics with line charts and insights

            get_page_header("Growth Metrics", "Year-over-year growth rates for key financial metrics.")

            tabs = st.tabs(GROWTH_LABELS)
            insights = growth_insights(GROWTH_LABELS)

            for tab, label in zip(tabs, GROWTH_LABELS):
                with tab:
                    series1 = get_growth_metrics(financials, cash_flows, label)

                    if series1 is not None:
                        # calculate growth (pct change) series based on retrieved metric series
                        growth = calculate_growth_series(series1)
                        growth_line_chart(ticker1, growth)

                        if label in insights:
                            st.caption(insights[label])

                        # if comparing, get growth metrics for second ticker and display side by side
                        if ticker2:
                            series2 = get_growth_metrics(financials2, cash_flows2, label)
                            df = pd.concat([series1, series2], axis=1).dropna()

                            df.columns = [ticker1_name, ticker2_name]

                            # format diluted EPS for easier comparison of numbers
                            if not label == "Diluted EPS":
                                df = df.style.format(format_large_number)
                            
                            st.markdown(f"<hr style='margin-top: 5px; margin-bottom: 20px; border: 2px solid #181C24;'>", unsafe_allow_html=True)
                            st.text(f"Comparing {label} Over Time")
                            st.dataframe(df)
                        
                    else:
                        st.caption(f"⚠️ {label} data not available.")


        # -----------------------------------
        #   Valuation Metrics -- DONE
        # -----------------------------------
        elif display == "Valuation Metrics":
            # Display valuation metrics and insights or compare between two companies

            get_page_header("Valuation Metrics", "Key valuation metrics to assess stock price relative to earnings and growth.")

            # Get valuation calculations as series, good for scalability
            valuation_series1 = get_valuation_metrics(ticker1)

            if ticker2:
                valuation_series2 = get_valuation_metrics(ticker2)
                col_display_metric(ticker_names, valuation_series1, valuation_series2)
            else:
                insights = valuation_insights(valuation_series1)
                col_display_insights(ticker1_name, valuation_series1, insights)
                

        # -----------------------------------
        #   Stock Metrics
        # -----------------------------------
        elif display == "Stock Performance Metrics":
            # Display the share price and metrics for one or two companies

            get_page_header("Stock Performance Metrics", "Historical stock price performance and key stock metrics.")

            stock_series1 = calculate_stock_metrics(hist1)

            if ticker2:
                plot_stocks(ticker1, ticker2)
                stock_series2 = calculate_stock_metrics(hist2)
                col_display_metric(ticker_names, stock_series1, stock_series2)
            else:
                plot_stocks(ticker1)
                display_MetricData(ticker1_name, stock_series1)

            # display cumilative return graph

        
        # -----------------------------------
        #   Cash Flow & Efficiency
        # -----------------------------------
        elif display == "Cash Flow & Efficiency":
            # Display 1-4 company metrics side by side for comparison


            # Allow user to compare up to enter 2 additional companies in sidebar
            ticker3 = st.sidebar.text_input("Enter Third Ticker").upper()
            ticker4 = st.sidebar.text_input("Enter Fourth Ticker").upper()
            
            get_page_header("Cash Flow & Efficiency Metrics", "Key cash flow and efficiency metrics to assess company performance.")

            if not ticker2 and (not ticker3 or not ticker4):
                st.info("Enter 1-3 additional ticker symbols in the sidebar to compare efficiency metrics across multiple companies.")
            
            efficiency_metrics1 = calculate_efficiency_metrics(cash_flows, financials, balance_sheet)
            insights = efficiency_insights(efficiency_metrics1)
            
            # Gather efficiency metrics for all companies to compare
            companies = {ticker1: efficiency_metrics1}
            if ticker2:
                efficiency_metrics2 = calculate_efficiency_metrics(cash_flows2, financials2, balance_sheet2)
                companies[ticker2] = efficiency_metrics2
            if ticker3:
                financials3, balance_sheet3, cash_flows3 = get_financial_statements(ticker3)
                efficiency_metrics3 = calculate_efficiency_metrics(cash_flows3, financials3, balance_sheet3)
                companies[ticker3] = efficiency_metrics3
            if ticker4:
                financials4, balance_sheet4, cash_flows4 = get_financial_statements(ticker4)
                efficiency_metrics4 = calculate_efficiency_metrics(cash_flows4, financials4, balance_sheet4)
                companies[ticker4] = efficiency_metrics4

            # display key for highlight colors
            st.markdown("""
                <ul style='font-size:0.8rem; padding-left: 20px;'>
                <li>
                    Low Outlier: <span style='color: lightcoral; padding: 2px 6px;'>Below normal range</span>
                </li>
                <li>
                    High Outlier: <span style='color: yellow; padding: 2px 6px;'>Above normal range</span>
                </li>
                </ul>
                """, 
                unsafe_allow_html=True
            )
      
            for label in CF_LABELS:
                st.subheader(label)

                if label in insights:
                    st.caption(insights[label])

                df = pd.DataFrame({comp: companies[comp][label] for comp in companies if companies[comp][label] is not None})
                df.index.name = 'Year'

                # Ensure df is correctly styled based on format needeed for output
                if label == "Free Cash Flows":
                    styled_df = df.style.format(format_large_number)
                elif label == "FCF Margin" or label == "Operating Margin":
                    styled_df = highlight_df_bounds(df, lower=CF_BOUNDS[label][0], upper=CF_BOUNDS[label][1]).format("{:.2%}")
                else:
                    styled_df = highlight_df_bounds(df, lower=CF_BOUNDS[label][0], upper=CF_BOUNDS[label][1])
                
                st.dataframe(styled_df)


    else:
        # Landing view. Give overview of what each Display does
        get_page_header("Overview", )
        st.markdown("""
            <p>Enter primary ticker symbol to analyze and compare key financial metrics for publicly traded companies. All data is up to date, retrieved from Yahoo Finance.</p>
            <p style='margin-top: -0.75rem'>Common Ticker Symbols:</p>
            <ul style='font-size:1rem; padding-left: 20px;'>
                <li> AAPL: Apple Inc. </li>
                <li> MSFT: Microsoft Corporation </li>
                <li> AMZN: Amazon.com, Inc. </li>
                <li> GOOG: Alphabet Inc. (Class C) </li>
            </ul>
            """, 
            unsafe_allow_html=True
        )
        st.markdown("""
            <h4>Analysis Options:</h4>
                <h6 style='color: #5C6B9C'>Core Financial Ratios</h6>
                    <ul style='font-size:1rem; padding-left: 20px;'>
                        <li> View key financial ratios and corresponding insights or compare ratios between two companies. </li>
                        <li> Profit Margin, ROE, Debt-to-Equity, Current Ratio, Quick Ratio</li>
                    </ul>
                <h6 style='color: #5C6B9C'>Growth Metrics</h6>
                    <ul style='font-size:1rem; padding-left: 20px;'>
                        <li> Displays graphs of year-over-year growth rates for key financial metrics.</li>
                        <li> Total Revenue, Net Income, Diluted EPS, Free Cash Flows </li>
                    </ul>
                <h6 style='color: #5C6B9C'>Valuation Metrics</h6>
                    <ul style='font-size:1rem; padding-left: 20px;'>
                        <li> View valuation metrics and corresponding insights or compare metrics between two companies.</li>
                        <li> Trailing P/E, Forward P/E, PEG Ratio, Price-to-Book, Enterprise Value, Market Cap, EV/EBITA, EV/Revenue </li>
                    </ul>
                <h6 style='color: #5C6B9C'>Stock Performance Metrics</h6>
                    <ul style='font-size:1rem; padding-left: 20px;'>
                        <li> Displays graph of closing price of shares and stock performance metrics for primary ticker and optional compare ticker.</li>
                        <li> Closing price over last year, volatility, Sharpe Ratio, Max Drawdown, Cumulative Return </li>
                    </ul>
                <h6 style='color: #5C6B9C'>Cash Flows & Efficiency</h6>
                    <ul style='font-size:1rem; padding-left: 20px;'>
                        <li> Displays tables of 1-4 companies comparing efficiency metrics and highlighting outliers outside of standard range.</li>
                        <li> Free Cash Flows, FCF Margin, Operating Margin, Asset Turnover </li>
                    </ul>
            """, 
            unsafe_allow_html=True
        )

        if ticker1 and not ticker_exists(ticker1):
            st.sidebar.warning("Please enter a valid primary ticker symbol")
        else:
            st.sidebar.info("Enter a primary ticker symbol to begin analysis.")


main()
