# utils/constants.py

PM = "Profit Margin"
ROE = "ROE"
DE = "Debt-to-Equity"
CR = "Current Ratio"
QR = "Quick Ratio"

RATIO_LABELS = [PM, ROE, DE, CR, QR]

REVENUE = "Total Revenue"
NET_INCOME = "Net Income"
DILUTED_EPS = "Diluted EPS"
FCF = "Free Cash Flows"

GROWTH_LABELS = [REVENUE, NET_INCOME, DILUTED_EPS, FCF]

FCF_MARGIN = "FCF Margin"
OP_MARGIN = "Operating Margin"
AT = "Asset Turnover"
INTEREST_COVERAGE = "Interest Coverage"
CF_LABELS = [FCF, FCF_MARGIN, OP_MARGIN, AT]

CF_BOUNDS = {
    FCF: None,
    FCF_MARGIN: (.05, .20),  # typical FCF margin is between 5% and 15-20%
    OP_MARGIN: (.1, .30), # typical operating margin is between 10% and 25-30%
    AT: (0.5, 2.0), # typical asset turnover is between 0.5 and 2.0
    INTEREST_COVERAGE: (1, None)  # generally, a ratio above 1.5 is considered good
}

TRAILING_PE = "Trailing P/E"
FORWARD_PE = "Forward P/E"
PEG = "PEG Ratio"
PB = "Price-to-Book"
ENTERPRISE_VALUE = "Enterprise Value"
MARKET_CAP = "Market Cap"
EV_EBITDA = "EV/EBITDA"
EV_REVENUE = "EV/Revenue"


VALUATION_LABELS = [TRAILING_PE, FORWARD_PE, PEG, PB, ENTERPRISE_VALUE, MARKET_CAP, EV_EBITDA, EV_REVENUE]

VOLATILITY = "Volatility"
SHARPE_RATIO = "Sharpe Ratio"
MAX_DRAWDOWN = "Max Drawdown"
CUMULATIVE_RETURN = "Cumulative Return"

STOCK_LABELS = [VOLATILITY, SHARPE_RATIO, MAX_DRAWDOWN, CUMULATIVE_RETURN]

