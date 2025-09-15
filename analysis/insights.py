# analysis/insights.py

from utils.constants import *  # Import all constants
import streamlit as st
# from data.metric_data import MetricData

def ratio_insights(d: dict):
    insights = {}

    if PM in d:
        val = d[PM].value
        # st.text(val)
        if val is not None:
            if val > 0.2: insights[PM] = "High Profit Margin: The company is very efficient at converting revenue into actual profit."
            elif val > 0.1: insights[PM] = "Moderate Profit Margin: The company has a decent level of profitability."
            elif val > 0: insights[PM] = "Low Profit Margin: The company is barely profitable and may struggle to cover costs."
            else: insights[PM] = "Negative Profit Margin: The company is operating at a loss."
    if ROE in d:
        val = d[ROE].value
        if val is not None:
            if val > 0.15: insights[ROE] = "Strong ROE: The company is effectively using shareholders' equity to generate profits."
            elif val > 0.1: insights[ROE] = "Average ROE: The company has a reasonable return on equity."
            elif val > 0: insights[ROE] = "Weak ROE: The company is generating low returns on shareholders' equity."
            else: insights[ROE] = "Negative ROE: The company is not generating profits from shareholders' equity."
    if DE in d:
        val = d[DE].value
        if val is not None:
            if val < 0.5: insights[DE] = "Low Debt-to-Equity: The company has a conservative capital structure with low reliance on debt."
            elif val < 1: insights[DE] = "Moderate Debt-to-Equity: The company has a balanced approach to using debt and equity for financing."
            else: insights[DE] = "High Debt-to-Equity: The company is heavily reliant on debt, which may increase financial risk."
    if CR in d:
        val = d[CR].value
        if val is not None:
            if val > 2: insights[CR] = "Strong Current Ratio: The company has a strong ability to cover its short-term liabilities with short-term assets."
            elif val > 1: insights[CR] = "Adequate Current Ratio: The company can meet its short-term obligations, but may face liquidity issues."
            else: insights[CR] = "Weak Current Ratio: The company may struggle to cover its short-term liabilities, indicating potential liquidity problems."
    if QR in d:
        val = d[QR].value
        if val is not None:
            if val > 1: insights[QR] = "Strong Quick Ratio: The company has a solid liquidity position, able to cover short-term liabilities without relying on inventory."
            elif val > 0.5: insights[QR] = "Adequate Quick Ratio: The company can meet its short-term obligations, but may face liquidity issues if inventory cannot be quickly converted to cash."
            else: insights[QR] = "Weak Quick Ratio: The company may struggle to cover its short-term liabilities, indicating potential liquidity problems."

    return insights

def growth_insights(d: dict):
    pass

def valuation_insights(d: dict):
    insights = {}

    if PEG in d:
        val = d[PEG].value
        if val is not None:
            if val < 1: insights[PEG] = "Undervalued: The stock may be undervalued relative to its earnings growth, potentially a good investment opportunity."
            elif val < 2: insights[PEG] = "Fairly Valued: The stock appears to be reasonably valued in relation to its earnings growth."
            else: insights[PEG] = "Overvalued: The stock may be overvalued relative to its earnings growth, which could indicate a higher risk investment."

    if TRAILING_PE in d:
        val = d[TRAILING_PE].value
        if val is not None:
            if val < 15: insights[TRAILING_PE] = "Low P/E Ratio: The stock may be undervalued or the company is experiencing challenges."
            elif val < 25: insights[TRAILING_PE] = "Average P/E Ratio: The stock is fairly valued compared to the market."
            else: insights[TRAILING_PE] = "High P/E Ratio: The stock may be overvalued or investors expect high growth."

    if FORWARD_PE in d:
        val = d[FORWARD_PE].value
        if val is not None:
            if val < 15: insights[FORWARD_PE] = "Low Forward P/E Ratio: The stock may be undervalued based on future earnings expectations."
            elif val < 25: insights[FORWARD_PE] = "Average Forward P/E Ratio: The stock is fairly valued based on future earnings expectations."
            else: insights[FORWARD_PE] = "High Forward P/E Ratio: The stock may be overvalued based on future earnings expectations."

    if PB in d:
        val = d[PB].value
        if val is not None:
            if val < 1: insights[PB] = "Low Price-to-Book Ratio: The stock may be undervalued or the company has significant assets."
            elif val < 3: insights[PB] = "Average Price-to-Book Ratio: The stock is fairly valued compared to its book value."
            else: insights[PB] = "High Price-to-Book Ratio: The stock may be overvalued or investors expect high growth."

    if EV_EBITDA in d:
        val = d[EV_EBITDA].value
        if val is not None:
            if val < 10: insights[EV_EBITDA] = "Low EV/EBITDA Ratio: The company may be undervalued or has strong earnings relative to its enterprise value."
            elif val < 15: insights[EV_EBITDA] = "Average EV/EBITDA Ratio: The company is fairly valued compared to its earnings."
            else: insights[EV_EBITDA] = "High EV/EBITDA Ratio: The company may be overvalued or has weak earnings relative to its enterprise value."
    if EV_REVENUE in d:
        val = d[EV_REVENUE].value
        if val is not None:
            if val < 2: insights[EV_REVENUE] = "Low EV/Revenue Ratio: The company may be undervalued or has strong revenue relative to its enterprise value."
            elif val < 5: insights[EV_REVENUE] = "Average EV/Revenue Ratio: The company is fairly valued compared to its revenue."
            else: insights[EV_REVENUE] = "High EV/Revenue Ratio: The company may be overvalued or has weak revenue relative to its enterprise value."
    if MARKET_CAP in d:
        val = d[MARKET_CAP].value
        if val is not None:
            if val > 200_000_000_000: insights[MARKET_CAP] = "Mega Cap: The company is a market leader with significant resources and stability."
            elif val > 10_000_000_000: insights[MARKET_CAP] = "Large Cap: The company is well-established and likely to be stable."
            elif val > 2_000_000_000: insights[MARKET_CAP] = "Mid Cap: The company has growth potential but may be more volatile than larger companies."
            elif val > 300_000_000: insights[MARKET_CAP] = "Small Cap: The company may offer high growth potential but comes with higher risk and volatility."
            else: insights[MARKET_CAP] = "Micro Cap: The company is very small and may be highly speculative with significant risk."
            
    return insights