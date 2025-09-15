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