# Stock Compare

A CLI tool that analyzes individual stocks or compares two side-by-side using live market data, then generates a self-contained HTML report you can open in any browser.

![Stock comparison report](screenshot.png)

## What it does

Choose between two modes:

**Single stock report** — get a full breakdown of one ticker including price history, volatility, beta, and a plain-English stability summary.

**Stock comparison** — compare two tickers side-by-side to quickly see which is more stable and which has delivered more growth. Useful for picking between two stocks in the same industry.

Metrics included for both modes:
- Current price, market cap, and P/E ratio
- Beta, dividend yield, and 52-week range
- 1-year return and annualized volatility
- 1-year price history chart

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

You'll be prompted to choose a mode, then enter one or two ticker symbols (e.g. `AAPL`, `MSFT`). The report is saved as `report.html` in the same directory — open it in any browser.

## Stack

- Python
- [yfinance](https://github.com/ranaroussi/yfinance) — market data
- [Chart.js](https://www.chartjs.org/) — price history chart (loaded via CDN)
