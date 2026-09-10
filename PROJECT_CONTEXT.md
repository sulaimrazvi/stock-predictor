# Project Context: Stock Predictor

> This file is the single source of truth for project state across sessions.
> Update the "Progress Log" and "Current State" sections manually as you go.
> Paste this whole file at the start of a new chat to restore context instantly.

## 1. Vision

A stock prediction dashboard for NSE stocks:
- Search/select stocks to track
- Fetch price + fundamental data
- Engineer technical features (RSI, MACD, moving averages, volatility, etc.)
- Train a model to predict direction (positive/negative) of a stock
- Separately scrape financial news/insight sites, run sentiment/NLP on them
- Fuse model prediction + sentiment signal + raw features into one dashboard view
- All shown in a UI where features, model prediction, and sentiment prediction are visible side by side

## 2. Tech Decisions (and why)

| Decision | Choice | Reasoning |
|---|---|---|
| Data source | `yfinance` (free) | Free, easy NSE access via `.NS` suffix, good enough to start |
| UI framework | Streamlit | Fast to build, pure Python, no separate frontend needed, sufficient for personal/prototype use |
| Backend API (FastAPI/Flask) | **Not used yet** | Not needed until: (a) predictions need to be consumed outside Streamlit, (b) multiple concurrent users, (c) heavy async/background compute. Revisit later — see "Future Considerations". |
| Project structure | Modular folders (`data/`, `features/`, `models/`, `ui/`) | Keeps data-fetch, feature-engineering, modeling, and UI decoupled so each step drops in cleanly |

## 3. Folder Structure

```
stock_predictor/
├── data/
│   ├── __init__.py
│   └── fetch.py          # search_stock(), get_price_history(), get_stock_info()
├── features/
│   └── __init__.py       # (empty - Step 2)
├── models/
│   └── __init__.py       # (empty - Step 3)
├── ui/
│   └── app.py            # Streamlit dashboard
├── requirements.txt
├── README.md
└── PROJECT_CONTEXT.md     # (this file)
```

## 4. Roadmap / Steps

- [x] **Step 1: Data fetching + basic UI** — yfinance integration, stock search, price history,
      fundamentals, Streamlit dashboard with candlestick chart. **DONE, tested, working.**
- [ ] **Step 2: Feature engineering** — RSI, MACD, moving averages, volatility, volume trends,
      computed from OHLCV data. Goes in `features/`. Display new columns on dashboard.
- [ ] **Step 3: Baseline prediction model** — define label (e.g. next-day/next-week return direction),
      train baseline model (logistic regression / random forest) on engineered features.
      Goes in `models/`.
- [ ] **Step 4: Web scraping + sentiment model** — scrape financial news/insight sites,
      train/use an NLP sentiment model on scraped text, separate from the price-based model.
- [ ] **Step 5: Fusion layer** — combine price-model prediction + sentiment signal into
      one combined view/score.
- [ ] **Step 6: Full dashboard** — show features + price-model prediction + sentiment prediction
      together per stock.
- [ ] **Step 7 (later, optional)**: Consider FastAPI backend IF predictions need to be
      consumed outside Streamlit, or multiple users, or heavier async compute needed.

## 5. Learning Approach (important - how we work together)

Goal: understand every line by the end of the project, not just have a working app.
Process for each new step:
1. Concept explained first (what + why)
2. Skeleton/function signatures given with TODOs, not full implementations
3. User writes the implementation themselves
4. User runs/debugs it
5. Review + correction together
6. Move to next step

(Exception: Step 1 was fully written by AI to get a working starting point fast — from Step 2
onward, follow the skeleton approach above.)

## 6. Progress Log

<!-- Add a dated entry each session. Keep it brief - just what changed and any decisions made. -->

- **2026-09-10**: Pushed Step 1 to GitHub (github.com/sulaimrazvi/stock-predictor).
  Fixed .gitignore issue (venv `env/` folder was initially staged - resolved with
  git reset + proper .gitignore before re-adding). Set up Claude Project with
  PROJECT_CONTEXT.md + custom instructions for skeleton-based learning workflow.
  Decided to do future steps in fresh chats within the Project, not one long chat.

## 7. Current State (update this section as the "latest snapshot")

- **Last completed step**: Step 1 (data fetch + basic UI) - done, tested, pushed to GitHub
- **Next step**: Step 2 - Feature engineering (RSI, MACD, moving averages, volatility, etc.)
  in `features/` folder, following skeleton-based learning approach (concept + skeleton,
  user implements, then review)
- **Repo**: https://github.com/sulaimrazvi/stock-predictor
- **Open questions / decisions pending**: None currently
- **Known issues**: None currently

## 8. Context Snapshot (for pasting into new AI sessions)

> Copy everything below this line into a new chat if starting fresh:

---
I'm building a stock predictor project (NSE stocks). Tech: Python, yfinance for data,
Streamlit for UI, modular folder structure (`data/`, `features/`, `models/`, `ui/`).
Step 1 (data fetch + search + basic dashboard) is done and working. Not using FastAPI yet
(deferred until a real need for external API access arises). I want to learn as I build -
give me concepts + skeleton code with TODOs, not full solutions, unless I ask for the
full solution after trying myself. Next step: [Step 2 - feature engineering / whatever is next].
---
