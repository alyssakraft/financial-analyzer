import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt


class Analyzer:
    # initialize ticker_symbol and ticker
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        self.ticker = yf.Ticker(ticker_symbol)

        self._financials = None
        self._balance_sheet = None
        self._revenue = None
        self._net_income = None
        self._equity = None
        self._debt = None
        self._ratios = None

    # lazy load remaining variables
    @property
    def financials(self):
        if self._financials is None:
            self._financials = self.ticker.financials
        return self._financials

    @property
    def balance_sheet(self):
        if self._balance_sheet is None:
            self._balance_sheet = self.ticker.balance_sheet
        return self._balance_sheet

    @property
    def revenue(self):
        if self._revenue is None:
            self._revenue = self.get_row_safe('Total Revenue')
        return self._revenue

    @property
    def net_income(self):
        if self._net_income is None:
            self._net_income = self.get_row_safe('Net Income')
        return self._net_income

    @property
    def equity(self):
        if self._equity is None:
            self._equity = self.get_row_safe_balance('Stockholders Equity')
        return self._equity

    @property
    def debt(self):
        if self._debt is None:
            self._debt = self.get_row_safe_balance('Total Debt')
        return self._debt

    @property
    def ratios(self):
        if self._ratios is None:
            self._ratios = self.calculate_ratios()
        return self._ratios

    # check for rows in financials containing row_name, return all matching
    def get_row_safe(self, row_name):
        matches = [r for r in self.financials.index if row_name.lower()
                   in r.lower()]

        if matches:
            return self.financials.loc[matches[0]].dropna()
        return pd.Series(type=float)

    # if row exists in ticker.balance_sheet, return row
    def get_row_safe_balance(self, row_name):
        matches = [r for r in self.balance_sheet.index if row_name.lower()
                   in r.lower()]
        if matches:
            return self.balance_sheet.loc[matches[0]].dropna()
        return pd.Series(dtype=float)

    def plot_financials(self, data: dict, scale="auto"):
        for name, series in data.items():
            if series is None or series.empty:
                st.warning(f"No data available for {name}")
                continue

            s = series.sort_index().copy()

            if scale == "auto":
                max_val = s.max()
                if max_val >= 1e9:
                    s_scaled = s / 1e9
                    unit = "Billion USD"
                elif max_val >= 1e6:
                    s_scaled = s / 1e6
                    unit = "Million USD"
                else:
                    s_scaled = s
                    unit = "USD"
            else:
                s_scaled = s / scale
                unit = f"USD / {scale}"

            df = pd.DataFrame({
                "Year": series.index.year,  # just the year
                name: s_scaled.values
            })

            ymax = df[name].max() * 1.05
            ymin = df[name].min() * 0.95

            chart = (
                alt.Chart(df)
                .mark_line(point=True)
                .encode(
                    x=alt.X("Year:O", title="Fiscal Year"),
                    y=alt.Y(f"{name}:Q", title=f"{name} ({unit})",
                            scale=alt.Scale(domain=[ymin, ymax])),
                    tooltip=["Year", name]
                )
            )

            st.subheader(f"{name} Over Time")
            # st.subheader(f"{self.ticker_symbol} {name} ({unit})")
            # st.line_chart(df, x_label="Year", y_label=unit)
            st.altair_chart(chart, use_container_width=True)
            # st.text(f"")

    def calculate_ratios(self):
        PM = self.net_income / self.revenue
        ROE = self.net_income / self.equity
        D_E = self.debt / self.equity

        print(f"equity = {self.equity}")
        print(f"debt = {self.debt}")

        PM.name = 'PM'
        ROE.name = 'ROE'
        D_E.name = "D/E"

        PM = PM.dropna()
        ROE = ROE.dropna()
        D_E = D_E.dropna()

        # st.table(pd.concat([PM, ROE, D_E], axis=1))

        return pd.concat([PM, ROE, D_E], axis=1)

    def compare_ratios(self, other):
        other.ratios

        s = self.ratios
        o = other.ratios
        s.index = s.index.year
        o.index = o.index.year

        # for var in ['PM', 'ROE', 'D/E']:
        #     st.text(var)
        #     compare = pd.concat(
        #         [self.ratios[var], other.ratios[var]], axis=1).dropna()
        #     compare.columns = [self.ticker_symbol, other.ticker_symbol]
        #     # st.text(self.ratios[var])
        #     st.dataframe(compare)
