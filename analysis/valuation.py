from data.fetcher import get_company_info
from utils.constants import TRAILING_PE, FORWARD_PE, PEG, PB, ENTERPRISE_VALUE, MARKET_CAP, EV_EBITDA, EV_REVENUE
from utils.formatter import format_large_number
from data.metric_data import MetricData
import streamlit as st

def calculate_forward_peg(info):
    """PE / Earnings Growth"""
    pe = info.get("forwardPE")
    growth = info.get("earningsGrowth")

    if pe is not None and growth:
        return pe / (growth * 100) if growth != 0 else None
    return None

# store valuation metrics in cache for performance
@st.cache_data
def get_valuation_metrics(ticker):
    """Calculate valuation metrics and return as a series."""

    info = get_company_info(ticker)

    series =  {
        TRAILING_PE: MetricData(TRAILING_PE, info.get("trailingPE")),
        FORWARD_PE: MetricData(FORWARD_PE, info.get("forwardPE")),
        PEG: MetricData(PEG, info.get("pegRatio")),
        PB: MetricData(PB, info.get("priceToBook")),
        ENTERPRISE_VALUE: MetricData(ENTERPRISE_VALUE, info.get("enterpriseValue"), fmt=format_large_number, suffix=" USD"),
        MARKET_CAP: MetricData(MARKET_CAP, info.get("marketCap"), fmt=format_large_number, suffix=" USD"),
        EV_EBITDA: MetricData(EV_EBITDA, info.get("enterpriseToEbitda")),
        EV_REVENUE: MetricData(EV_REVENUE, info.get("enterpriseToRevenue"))
    }

    if series[PEG].value == None:
        series[PEG] = MetricData(PEG, calculate_forward_peg(info))

    return series


