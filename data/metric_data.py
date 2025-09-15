class MetricData:
    def __init__(self, name, value, delta=None, fmt="{:.2f}", suffix=""):
        self.name = name
        self.value = value
        self.delta = delta
        self.fmt = fmt
        self.suffix = suffix
    
    def formatted_value(self):
        if callable(self.fmt):
            return self.fmt(self.value) + self.suffix
        return self.fmt.format(self.value) + self.suffix