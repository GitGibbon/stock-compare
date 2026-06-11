import yfinance as yf


def fetch_stock_data(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info
    history = stock.history(period="1y")

    if history.empty:
        raise ValueError(f"No data found for ticker '{ticker}'. Check that it's a valid symbol.")

    daily_returns = history["Close"].pct_change().dropna()
    annualized_volatility = daily_returns.std() * (252 ** 0.5)
    one_year_return = (history["Close"].iloc[-1] - history["Close"].iloc[0]) / history["Close"].iloc[0]

    return {
        "ticker": ticker.upper(),
        "name": info.get("longName") or ticker.upper(),
        "price": info.get("currentPrice") or info.get("regularMarketPrice"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "beta": info.get("beta"),
        "dividend_yield": info.get("dividendYield"),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
        "one_year_return": one_year_return,
        "volatility": annualized_volatility,
        "history_dates": history.index.strftime("%Y-%m-%d").tolist(),
        "history_prices": history["Close"].round(2).tolist(),
    }
