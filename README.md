# Stock Predictor

A stock prediction dashboard: fetch NSE stock data, engineer features, predict direction with ML,
and cross-check against scraped market sentiment.

## Setup

```bash
pip install -r requirements.txt
```

## Run the dashboard

```bash
streamlit run ui/app.py
```

## Project structure

```
stock_predictor/
├── data/           # Data fetching (yfinance for now)
│   └── fetch.py
├── features/        # Technical indicators & engineered features (Step 2)
├── models/           # Prediction models (Step 3)
├── ui/              # Streamlit dashboard
│   └── app.py
├── requirements.txt
└── README.md
```

## Roadmap

- [x] Step 1: Data fetching (yfinance) + search + basic UI
- [ ] Step 2: Feature engineering (RSI, MACD, moving averages, volatility, etc.)
- [ ] Step 3: Baseline prediction model (direction: up/down)
- [ ] Step 4: Web scraping + sentiment model from financial news/insight sites
- [ ] Step 5: Fusion layer (combine model prediction + sentiment signal)
- [ ] Step 6: Full dashboard (predictions + sentiment + features together)
