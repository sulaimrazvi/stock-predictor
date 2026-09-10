import pandas as pd

def add_moving_averages(df: pd.DataFrame, windows: list[int] = [20, 50, 100, 150])-> pd.DataFrame:
    """
    Add Simple Moving Average (SMA) columns for each window.

    Adds columns like: SMA_20, SMA_50

    Args:
        df: DataFrame with at least a 'Close' column
        windows: list of lookback periods in days

    Returns:
        df with new SMA columns added (does not drop original columns)
    """
    # TODO: for each window in windows, compute rolling mean of 'Close'
    # and store in a column named f"SMA_{window}"
    for window in windows:
        df[f"SMA_{window}"] = df['Close'].rolling(window=window).mean()
        
    return df

def add_ema(df: pd.DataFrame, windows: list[int] = [12, 26]) -> pd.DataFrame:
    """
    Add Exponential Moving Average (EMA) columns.

    Adds columns like: EMA_12, EMA_26

    Args:
        df: DataFrame with a 'Close' column
        windows: list of spans (in days)

    Returns:
        df with new EMA columns added
    """
    # TODO: use pandas ewm(span=window, adjust=False).mean()
    for window in windows:
        df[f"EMA_{window}"] = df["Close"].ewm(span=window, adjust=False).mean()
    return df


def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Add RSI (Relative Strength Index) column.

    RSI = 100 - (100 / (1 + RS)) where RS = avg_gain / avg_loss
    over `period` days.

    Adds column: RSI_14 (or RSI_{period})

    Args:
        df: DataFrame with a 'Close' column
        period: lookback window (default 14 is standard)

    Returns:
        df with RSI column added
    """
    # TODO:
    # 1. Compute daily price change: delta = Close.diff()
    # 2. Separate gains (delta > 0) and losses (delta < 0, take abs)
    # 3. Compute rolling mean of gains and losses over `period`
    #    Hint: use ewm(com=period-1, adjust=False) — more standard than simple rolling mean for RSI
    # 4. RS = avg_gain / avg_loss
    # 5. RSI = 100 - (100 / (1 + RS))
    delta = df['Close'].diff()
    gain = delta.where(delta>0,0)
    loss= delta.where(delta<0,0).abs()
    avg_gain=gain.ewm(com=period-1, adjust=False).mean()
    avg_loss=loss.ewm(com=period-1,adjust=False).mean()
    rs=avg_gain/avg_loss
    df[f"RSI_{period}"] = 100 - (100 / (1 + rs))
    return df


def add_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """
    Add MACD, Signal line, and Histogram columns.

    MACD = EMA(fast) - EMA(slow)
    Signal = EMA(MACD, signal)
    Histogram = MACD - Signal

    Adds columns: MACD, MACD_Signal, MACD_Hist

    Args:
        df: DataFrame with a 'Close' column
        fast: short EMA span (default 12)
        slow: long EMA span (default 26)
        signal: EMA span for signal line (default 9)

    Returns:
        df with MACD columns added
    """
    # TODO: build on your EMA logic from add_ema
    ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
    df['MACD'] = ema_fast - ema_slow
    df['MACD_Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
    return df


def add_volatility(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Add rolling volatility (std of daily returns) column.

    Adds column: Volatility_20

    Args:
        df: DataFrame with a 'Close' column
        window: rolling window in days

    Returns:
        df with Volatility column added
    """
    # TODO:
    # 1. Compute daily returns: pct_change()
    # 2. Rolling std over `window`
    df['Daily_Return']= df['Close'].pct_change()
    df[f"Volatility_{window}"] = df['Daily_Return'].rolling(window=window).std()
    return df


def add_volume_features(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Add volume-based features.

    Adds columns:
        Volume_SMA_20  — rolling average volume
        Volume_Ratio   — today's volume / rolling average (is volume unusual?)

    Args:
        df: DataFrame with a 'Volume' column
        window: rolling window for average volume

    Returns:
        df with volume feature columns added
    """
    # TODO: rolling mean of Volume, then ratio = Volume / rolling mean
    df[f'Volume_SMA_{window}'] = df['Volume'].rolling(window=window).mean()
    df[f'Volume_Ratio'] = df['Volume'] / df[f'Volume_SMA_{window}']
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Master function: applies all feature engineering steps in sequence.

    Args:
        df: raw OHLCV DataFrame from yfinance

    Returns:
        df with all engineered feature columns added, NaN rows dropped
    """
    # TODO: call each add_* function in sequence, then dropna() at the end
    # (NaNs appear at the start of rolling windows — that's expected and normal)
    df = add_moving_averages(df)
    df = add_ema(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_volatility(df)
    df = add_volume_features(df)
    df = df.dropna(subset=[
    "SMA_20", "SMA_50",
    "EMA_12", "EMA_26",
    "RSI_14",
    "MACD", "MACD_Signal", "MACD_Hist",
    "Volatility_20",
    "Volume_SMA_20", "Volume_Ratio"
])
    return df
