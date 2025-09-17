# format numbers, percentages, currency, etc.

def format_delta(current, previous, pct=False):
    if previous is [None, 0]:
        return None
    if pct:
        return (current - previous) / abs(previous) * 100
    else:
        return current - previous

def format_currency(value, currency="$", decimals=2):
    if value is None:
        return None
    return f"{currency}{value:,.{decimals}f}"

# format large numbers with K, M, B suffixes
def format_large_number(value):
    if value is None:
        return None
    abs_value = abs(value)
    if abs_value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f}T"
    elif abs_value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif abs_value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif abs_value >= 1_000:
        return f"{value / 1_000:.2f}K"
    else:
        return str(value)

    
def highlight_df_bounds(df, lower=None, upper=None, low_color='lightcoral', high_color='yellow'):
    numeric_cols = df.select_dtypes(include='number').columns

    def style_func(s):
        return [
            f'color: {low_color}' if (lower is not None and v < lower)
            else f'color: {high_color}' if (upper is not None and v > upper)
            else ''
            for v in s
        ]

    return df.style.apply(style_func, subset=numeric_cols)