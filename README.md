# Financial Analyzer

A web app for retrieving and analyzing company financial metrics, built with Streamlit and pandas, using real-time data from Yahoo Finance.

Link: https://ak-financial-analyzer.streamlit.app/

## Features

- Ticker Analysis: Pulls financial data using yfinance
- Ratio Calculations: Visualizes revenue and net income trends
- Growth Metrics: Computes ROE, Profit Margin, and D/E
- Peer Benchmarking: Compares metrics across selected tickers
- Outlier Detection: Highlights abnormal values with color-coded commentary
- Error Handling: Gracefully manages missing or malformed data

## Tech Stack

- **Frontend / UI**: [Streamlit](https://streamlit.io/)
- **Data Handling**: [pandas](https://pandas.pydata.org/)
- **Data Source**: [yfinance](https://pypi.org/project/yfinance/)
- **Language**: `Python 3.9+`

## Installation

##### 1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/financial-analyzer.git
   cd financial-analyzer
   ```
##### 2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```
##### 3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```
##### 4. Run the app
   ```bash
   streamlit run app.py
   ```

## Sample Usage

![App Screenshot] images/screenshot.png

## Project Structure

financial-analyzer/ 

├── app.py # Main Streamlit app entry point 

├── data/ 

|     ├── fetcher.py          # Retrieves and labels financial data from yfinance 

|     └── metric_data.py      # Defines metric labels and mappings 

├── analysis/ 

|     ├── growth.py           # Calculates revenue and net income growth metrics 

|     └── performance.py      # Computes efficiency metrics (FCF, margins, turnover) 

├── utils/ 

|     ├── formatter.py        # Formats numbers and commentary for display 

|     └── constants.py        # Stores metric keys and threshold bounds 

├── images/ 

|     └── screenshot.png      # App screenshot for README 

├── requirements.txt          # Dependency list for deployment 

└── README.md                 # Project overview and usage instructions

## Design Philosophy

This app was built with modularity and clarity in mind:

- Reusable functions for formatting, commentary and error handling
- Intuitive layout with labeled sections and dynamic tooltips
- Clean codebase for easy extension and review

## Future Enhancements

- Toggle between quarterly and annual data
- Export charts and commentary to pdf

## Author

Alyssa Kraft

[Github Profile](https://github.com/alyssakraft) [LinkedIn](www.linkedin.com/in/alyssa-g-kraft)
