"""
ui/app.py
---------
Simple Streamlit dashboard for the Stock Predictor project.

Run from the project root with:
    streamlit run ui/app.py

Features (Step 1 UI):
- Search for stocks by name/symbol
- Select a stock and view price chart (candlestick) + key fundamentals
- This is the foundation - prediction/sentiment sections get added in later steps
"""

import sys
import os

# Allow importing from the data/ folder regardless of where streamlit is launched from
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import plotly.graph_objects as go
from data.fetch import search_stock, get_price_history, get_stock_info

st.set_page_config(page_title="Stock Predictor", layout="wide")

st.title("📈 Stock Predictor Dashboard")
st.caption("Step 1: Search, view price history & fundamentals. Predictions coming in later steps.")

# --- Sidebar: Search ---
with st.sidebar:
    st.header("Search Stocks")
    query = st.text_input("Search by name or symbol", placeholder="e.g. Reliance, TCS, Infosys")

    selected_symbol = None
    if query:
        results = search_stock(query)
        if results:
            options = {f"{r['name']} ({r['symbol']}) - {r['exchange']}": r["symbol"] for r in results}
            choice = st.selectbox("Select a match", list(options.keys()))
            selected_symbol = options[choice]
        else:
            st.warning("No matches found.")

    st.divider()
    period = st.selectbox("Time period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=2)

# --- Main area ---
if selected_symbol:
    with st.spinner(f"Fetching data for {selected_symbol}..."):
        price_df = get_price_history(selected_symbol, period=period)
        info = get_stock_info(selected_symbol)

    curated = info["curated"]

    # Header row: name + key stats
    st.subheader(f"{curated.get('shortName', selected_symbol)} ({selected_symbol})")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Current Price", f"₹{curated.get('currentPrice', 'N/A')}")
    col2.metric("Sector", curated.get("sector", "N/A"))
    col3.metric("P/E (Trailing)", curated.get("trailingPE", "N/A"))
    col4.metric("52W High", curated.get("fiftyTwoWeekHigh", "N/A"))
    col5.metric("52W Low", curated.get("fiftyTwoWeekLow", "N/A"))

    # Candlestick chart
    if not price_df.empty:
        fig = go.Figure(data=[go.Candlestick(
            x=price_df["Date"],
            open=price_df["Open"],
            high=price_df["High"],
            low=price_df["Low"],
            close=price_df["Close"],
        )])
        fig.update_layout(
            title=f"{selected_symbol} Price History ({period})",
            xaxis_title="Date",
            yaxis_title="Price (INR)",
            height=500,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Volume chart
        vol_fig = go.Figure(data=[go.Bar(x=price_df["Date"], y=price_df["Volume"])])
        vol_fig.update_layout(title="Volume", height=250)
        st.plotly_chart(vol_fig, use_container_width=True)
    else:
        st.warning("No price data available for this period.")

    # Fundamentals table
    with st.expander("📊 Full Fundamentals"):
        st.json(curated)

    # Raw price data table
    with st.expander("📄 Raw Price Data"):
        st.dataframe(price_df, use_container_width=True)

else:
    st.info("👈 Search for a stock in the sidebar to get started.")
