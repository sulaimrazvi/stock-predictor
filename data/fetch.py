"""
data/fetch.py
-------------
Core data-fetching logic for the Stock Predictor project.
This module is imported by the UI (ui/app.py) and later by feature engineering / models.
Keeping it separate means we only write "get data from yfinance" logic ONCE.
"""

import yfinance as yf
import pandas as pd


def search_stock(query: str, limit: int = 8):
    """Search for stocks by name or symbol. Returns list of dicts."""
    if not query or len(query.strip()) < 2:
        return []
    results = yf.Search(query, max_results=limit).quotes
    cleaned = []
    for r in results:
        cleaned.append({
            "symbol": r.get("symbol"),
            "name": r.get("shortname") or r.get("longname"),
            "exchange": r.get("exchange"),
            "type": r.get("quoteType"),
        })
    return cleaned


def get_price_history(symbol: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """Fetch OHLCV data for a given symbol (NSE symbols need '.NS' suffix)."""
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=interval)
    df.reset_index(inplace=True)
    return df


def get_stock_info(symbol: str) -> dict:
    """Fetch fundamental info for a symbol. Returns curated + raw dict."""
    ticker = yf.Ticker(symbol)
    info = ticker.info

    useful_fields = [
        "shortName", "sector", "industry", "marketCap", "currency",
        "currentPrice", "previousClose", "open", "dayLow", "dayHigh",
        "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "volume", "averageVolume",
        "trailingPE", "forwardPE", "priceToBook", "dividendYield",
        "returnOnEquity", "debtToEquity", "profitMargins", "beta",
        "recommendationKey", "targetMeanPrice", "numberOfAnalystOpinions",
    ]
    curated = {k: info.get(k) for k in useful_fields}
    return {"curated": curated, "raw": info}
