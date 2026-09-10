"""
models/train.py
---------------
Baseline prediction model for Stock Predictor.

Pipeline:
  1. make_labels()          — adds Target column (1 = price up, 0 = price down)
  2. prepare_features()     — selects + cleans columns for training
  3. split_time_series()    — chronological train/test split (NO random shuffle)
  4. train_model()          — trains a chosen model, returns it + metrics
  5. evaluate_model()       — prints accuracy, precision, recall, confusion matrix

Usage (for testing in __main__):
  python -m models.train
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Don't import XGBoost at the top yet — add it when we get to that stage


def make_labels(df: pd.DataFrame, horizon: int = 5) -> pd.DataFrame:
    """
    Add a binary Target column to the dataframe.

    Target = 1 if Close[t + horizon] > Close[t], else 0.
    Rows where the future is unknown (last `horizon` rows) are dropped.

    Args:
        df:      DataFrame with at least a 'Close' column
        horizon: number of trading days to look ahead (default 5 = 1 week)

    Returns:
        DataFrame with new 'Target' column, last `horizon` rows dropped.

    TODO:
        - Use df['Close'].shift(-horizon) to get the future close price
        - Compare future close to current close to produce 1 or 0
        - Assign result to df['Target']
        - Drop the last `horizon` rows (they have NaN targets) using dropna()
        - Return the cleaned df
    """
    df['Target'] = (df['Close'].shift(-horizon) > df['Close']).astype(int)
    df = df.iloc[:-horizon]
    return df

def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """
    Split the dataframe into features (X) and label (y).
    Also drops columns that shouldn't be fed to the model.

    Args:
        df: DataFrame with engineered features AND a 'Target' column

    Returns:
        X: feature DataFrame
        y: Target series

    TODO:
        - Define a list of columns to DROP — think about which ones leak the future
          or are non-numeric / not useful:
            'Target', 'Date', 'Dividends', 'Stock Splits'
          (drop them if they exist, ignore if they don't — use errors='ignore')
        - Assign remaining columns to X
        - Assign df['Target'] to y
        - Return X, y
    """
    x=df.drop(columns=['Target', 'Date', 'Dividends', 'Stock Splits'], errors='ignore')
    y=df['Target']
    return x,y


def split_time_series(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2):
    """
    Chronological train/test split. NO shuffling.

    Args:
        X:         feature DataFrame
        y:         Target series
        test_size: fraction of data to use for test (default 0.2 = last 20%)

    Returns:
        X_train, X_test, y_train, y_test

    TODO:
        - Calculate split index: int(len(X) * (1 - test_size))
        - Slice X and y using that index (first part = train, rest = test)
        - Return the four splits
    """
    x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=test_size,shuffle=False)
    return x_train, x_test, y_train, y_test


def train_model(x_train, y_train, model_type: str = "random_forest"):
    """
    Train a model on the training data.

    Args:
        x_train:    training features
        y_train:    training labels
        model_type: one of 'logistic', 'random_forest' (xgboost added later)

    Returns:
        model:   the fitted model object
        scaler:  the fitted StandardScaler (needed to transform test data the same way)

    TODO:
        - Create a StandardScaler, fit on x_train, transform x_train
          (scaler must be fitted on train only — never on test data)
        - If model_type == 'logistic': create LogisticRegression(max_iter=1000)
        - If model_type == 'random_forest': create RandomForestClassifier(n_estimators=100, random_state=42)
        - Fit the model on scaled X_train and y_train
        - Return model, scaler
    """
    scaler=StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    if model_type == 'logistic':
        model = LogisticRegression(max_iter=1000)  
    elif model_type == 'random_forest':
        model = RandomForestClassifier(
                        n_estimators=200,
                        max_depth=10,
                        min_samples_split=10,
                        min_samples_leaf=5,
                        class_weight='balanced',
                        random_state=42
                    )
    elif model_type == 'xgboost':
        from xgboost import XGBClassifier
        model = XGBClassifier(
                        n_estimators=200,
                        max_depth=5,
                        learning_rate=0.05,
                        subsample=0.8,
                        colsample_bytree=0.8,
                        scale_pos_weight=1,
                        eval_metric='logloss',
                        random_state=42
                    )
    else:
        raise ValueError(f"Unknown model_type: {model_type}")
    model.fit(x_train_scaled, y_train)
    return model, scaler


def evaluate_model(model, scaler, x_test, y_test) -> dict:
    """
    Evaluate model on test data. Prints and returns key metrics.

    Args:
        model:   fitted model
        scaler:  fitted scaler from train_model()
        X_test:  test features (unscaled)
        y_test:  true test labels

    Returns:
        dict with accuracy, precision, recall, confusion_matrix

    TODO:
        - Scale X_test using scaler.transform() (NOT fit_transform — why?)
        - Get predictions: model.predict(X_test_scaled)
        - Compute accuracy, precision, recall using sklearn functions
        - Compute confusion matrix
        - Print all four values clearly
        - Return them as a dict
    """
    x_test_scaled = scaler.transform(x_test)
    preds=model.predict(x_test_scaled)
    accuracy = accuracy_score(y_test, preds)
    precision = precision_score(y_test, preds)
    recall = recall_score(y_test, preds)
    conf_matrix = confusion_matrix(y_test, preds)
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print("Confusion Matrix:")
    print(conf_matrix)
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "confusion_matrix": conf_matrix
    }


if __name__ == "__main__":
    # Quick end-to-end test — runs when you do: python -m models.train
    from data.fetch import get_price_history
    from features.engineer import engineer_features
    

    symbol = "RELIANCE.NS"
    print(f"Fetching data for {symbol}...")

    df = get_price_history(symbol, period="max")
    df = engineer_features(df)
    df = df.dropna()          # ← add this line
    df = make_labels(df, horizon=5)

    print(f"Rows after dropna: {len(df)}")
    print(f"NaN count:\n{df.isna().sum().sum()}")  # should be 0

    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = split_time_series(X, y)

    print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
    print(f"Label distribution:\n{y.value_counts()}")

    for model_type in ["logistic", "random_forest", "xgboost"]:
        print(f"\n--- {model_type.upper()} ---")
        model, scaler = train_model(X_train, y_train, model_type=model_type)
        metrics = evaluate_model(model, scaler, X_test, y_test)
        if model_type in ["random_forest", "xgboost"]:  # ← only these two
            importance = pd.Series(model.feature_importances_, index=X_train.columns)
            print(importance.sort_values(ascending=False).to_string())