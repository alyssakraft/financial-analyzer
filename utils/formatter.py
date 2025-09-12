# format numbers, percentages, currency, etc.

def format_delta(current, previous):
    if previous is [None, 0]:
        return None
    return (current - previous) / abs(previous) * 100