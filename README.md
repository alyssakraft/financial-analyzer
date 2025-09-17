# Financial Analyzer

A web app for retrieving and analyzing company financial metrics, built with Streamlit and pandas, using real-time data from Yahoo Finance.

---

## Features

- Ticker Analysis: Pulls financial data using yfinance
- Ratio Calculations: Visualizes revenue and net income trends
- Growth Metrics: Computes ROE, Profit Margin, and D/E
- Peer Benchmarking: Compares metrics across selected tickers
- Outlier Detection: Highlights abnormal values with color-coded commentary
- Error Handling: Gracefully manages missing or malformed data

---

## Tech Stack

- **Frontend / UI**: [Streamlit](https://streamlit.io/)
- **Data Handling**: [pandas](https://pandas.pydata.org/)
- **Data Source**: [yfinance](https://pypi.org/project/yfinance/)
- **Language**: Python 3.9+

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/financial-analyzer.git
   cd financial-analyzer
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Sample Usage

![App Screenshot] images/screenshot.png

## Design Philosophy

This app was built with modularity and clarity in mind:

- Reusable functions for formatting, commentary and error handling
- Intuitive layour with labeled sections and dynamic tooltips
- Clean codebase for easy extension and review

## Future Enhancements

- Toggle between quarter annual data
- Export charts and commentary to pdf

## Author

Alyssa Kraft
[Github Profile](https://github.com/alyssakraft) [LinkedIn](www.linkedin.com/in/alyssa-g-kraft)
