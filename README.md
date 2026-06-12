# Stock Compare

A CLI tool that compares two stocks side-by-side using live market data, then generates a self-contained HTML report you can open in any browser.

## What it does

Enter any two ticker symbols and get an instant comparison of:

- Current price, market cap, and P/E ratio
- Beta, dividend yield, and 52-week range
- 1-year return and annualized volatility
- 1-year price history chart
- A plain-English summary of which stock is more stable vs. higher growth

## Why I built it

Investors looking at two stocks in the same industry need a fast way to compare stability vs. growth potential. This tool generates that comparison in seconds with no login, no subscription, and no browser extension required.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

You'll be prompted for two ticker symbols (e.g. `AAPL` and `MSFT`). The report is saved as `report.html` in the same directory — open it in any browser.

## Stack

- Python
- [yfinance](https://github.com/ranaroussi/yfinance) — market data
- [Chart.js](https://www.chartjs.org/) — price history chart (loaded via CDN)
