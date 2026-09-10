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
- [x] **Step 2: Feature engineering** — RSI, MACD, moving averages (SMA 20/50/100/150),
      volatility, volume trends, computed from OHLCV data. **DONE, tested, working, and
      wired into `ui/app.py` with indicator charts.** Lives in `features/engineer.py`.
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

- **2026-09-10**: Pushed Step 1 to GitHub (github.com/sulaimrazvi/stock-predictor).
  Fixed .gitignore issue (venv `env/` folder was initially staged - resolved with
  git reset + proper .gitignore before re-adding). Set up Claude Project with
  PROJECT_CONTEXT.md + custom instructions for skeleton-based learning workflow.
  Decided to do future steps in fresh chats within the Project, not one long chat.

- **2026-09-11**: Completed Step 2 (feature engineering). Built `features/engineer.py`
  with `add_moving_averages`, `add_ema`, `add_rsi`, `add_macd`, `add_volatility`,
  `add_volume_features`, and master `engineer_features()`. Tested end-to-end on
  RELIANCE.NS — 20 columns produced correctly, RSI/Volume_Ratio values sanity-checked
  and look reasonable. Dropped SMA_100/SMA_150 for now (get_price_history() currently
  fetches ~129 rows / ~6mo, not enough history for 100/150-day windows to produce
  non-NaN values — every row got dropped when tested with them). Kept SMA_20/50 only.
  Decision: revisit longer SMA windows at Step 3 once fetch period is increased for
  model training (129 rows -> 79 after dropna is too small a dataset anyway).
  UI (`ui/app.py`) NOT yet wired to display new features — that's a separate future task,
  not part of Step 2 as scoped.

  - **2026-09-11 (cont'd)**: Re-added `SMA_100`/`SMA_150` to `add_moving_averages()` defaults
  after confirming `5y` period fetch gives enough history for them to compute properly.
  Fixed `engineer_features()` — changed blanket `df.dropna()` to `df.dropna(subset=[...])`
  with only short-window columns (SMA_20/50, EMA_12/26, RSI_14, MACD family, Volatility_20,
  Volume_SMA_20, Volume_Ratio) as required. SMA_100/150 now allowed to stay NaN early
  without wiping out otherwise-valid rows — fixes the earlier all-or-nothing dropna issue.
  Wired engineered features into `ui/app.py`: added `engineer_features(price_df.copy())`
  call, plus three new chart panels below the existing candlestick/volume charts —
  Price+MA overlay (SMA 20/50/100/150), RSI panel (with 30/70 reference lines), and
  MACD panel (MACD + Signal lines + Histogram bars). Tested visually on RELIANCE-type
  ticker with 5y period — SMA_100/150 lines correctly appear partway through the chart
  once enough history exists, short indicators populate from near the start.
  **Known issue found (not fixed yet)**: stock search for "reliance" matched a US-listed
  "Reliance, Inc. (RS) - NYQ" result instead of NSE's RELIANCE.NS — `search_stock()` in
  `data/fetch.py` may need better filtering/prioritization for NSE-only results.

## 7. Current State (update this section as the "latest snapshot")

- **Last completed step**: Step 2 (feature engineering) - done, tested, wired into UI
  with indicator charts (MA overlay, RSI, MACD panels), committed
- **Next step**: Step 3 - Baseline prediction model (define label, train logistic
  regression / random forest on engineered features) in `models/` folder. Will likely
  need to first increase `get_price_history()` fetch period (currently ~6mo/129 rows,
  too small for training) before starting Step 3.
- **Repo**: https://github.com/sulaimrazvi/stock-predictor
- - **Open questions / decisions pending**:
  - Confirm final fetch period to use for Step 3 model training (5y confirmed working
    for SMA_100/150; decide default period for `get_price_history()` going forward)
- **Known issues**:
  - `search_stock()` in `data/fetch.py` can match wrong-market tickers (e.g. US-listed
    "Reliance, Inc." instead of NSE's RELIANCE.NS) - needs NSE filtering/prioritization,
    not yet fixed

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
