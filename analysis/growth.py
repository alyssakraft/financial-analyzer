# revenue, net income, EPS growth

import pandas as pd

def calculate_growth_series(series):
    """
    Calculates year-over-year growth rates from a time series.
    Returns a Series of growth percentages.
    """
    return series.pct_change().dropna()

def get_metric_series(financials, label):
    """
    Extracts a time series for a given label from the financials DataFrame.
    Returns a Series indexed by year.
    """
    if label not in financials.index:
        return None

    series = financials.loc[label]
    # Ensure index is datetime or year
    if not isinstance(series.index[0], (int, float)):
        series.index = pd.to_datetime(series.index).year
    return series.sort_index()

def get_growth_metrics(financials):
    """
    Returns a dictionary of growth rates for key metrics.
    """
    metrics = {}
    for label in ["Total Revenue", "Net Income", "Diluted EPS", "Free Cash Flow"]:
        series = get_metric_series(financials, label)
        if series is not None:
            growth = calculate_growth_series(series)
            metrics[label] = growth
    return metrics
