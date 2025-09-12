from data.fetcher import get_company_info
from utils.constants import VALUATION_LABELS

def calculate_forward_peg(info):
    """PE / Earnings Growth"""
    pe = info.get("forwardPE")
    growth = info.get("earningsGrowth")

    if pe is not None and growth:
        return pe / (growth * 100) if growth != 0 else None
    return None

def get_valuation_metrics(ticker):
    """Calculate valuation metrics and return as a series."""

    info = get_company_info(ticker)

    series =  {
    "Trailing P/E": info.get("trailingPE"),
    "Forward P/E": info.get("forwardPE"),
    "PEG Ratio": info.get("pegRatio"),
    "Price-to-Book": info.get("priceToBook"),
    "Enterprise Value": info.get("enterpriseValue"),
    "Market Cap": info.get("marketCap"),
    "EV/EBITDA": info.get("enterpriseToEbitda"),
    "EV/Revenue": info.get("enterpriseToRevenue")
    }

    if series['PEG Ratio'] == None:
        series['PEG Ratio'] = calculate_forward_peg(info)

    return series


