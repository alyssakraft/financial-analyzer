"""
data/metric_data.py

Defines MetricData class for storing financial metric information.
"""

class MetricData:
    """A container for financial metric values with optional formatting and deltas."""

    def __init__(self, name, value, delta=None, fmt="{:.2f}", suffix=""):
        """
        Initialize a MetricData object.

        Args:
            name (str): Name of the metric.
            value (float): The numeric value of the metric.
            delta (float, optional): Change compared to a baseline value. Defaults to None.
            fmt (str or callable, optional): Format string or callable for displaying the value.
            suffix (str, optional): Text appended after the value (e.g., '%'). Defaults to "".
        """
        self.name = name
        self.value = value
        self.delta = delta
        self.fmt = fmt
        self.suffix = suffix
    
    def formatted_value(self):
        """Return formatted value as string."""
        if callable(self.fmt):
            return self.fmt(self.value) + self.suffix
        return self.fmt.format(self.value) + self.suffix