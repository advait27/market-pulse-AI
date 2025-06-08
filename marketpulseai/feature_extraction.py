# feature_extraction.py
import pandas as pd
import numpy as np


def compute_features(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Simulate key features similar to what finfeatures might generate.
    Assumes columns: Date, Open, High, Low, Close, Volume, ticker
    """
    df = df.copy()
    df.sort_values("Date", inplace=True)

    # Daily return
    df["daily_return"] = df["Close"].pct_change()

    # Rolling volatility (standard deviation of returns)
    df["rolling_volatility"] = df["daily_return"].rolling(window).std()

    # Momentum (difference between current close and window-day ago close)
    df["momentum"] = df["Close"] - df["Close"].shift(window)

    # Moving Average
    df["moving_avg"] = df["Close"].rolling(window).mean()

    # Relative Strength Index (RSI)-like (simplified version)
    delta = df["Close"].diff().astype(float)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window).mean()
    avg_loss = pd.Series(loss).rolling(window).mean()
    rs = avg_gain / (avg_loss + 1e-10)
    df["rsi"] = 100 - (100 / (1 + rs))

    # Volume Trend (moving average of volume)
    df["volume_avg"] = df["Volume"].rolling(window).mean()

    return df


if __name__ == "__main__":
    # Demo run with mock data
    df = pd.read_csv("mock_stock_data.csv")  # replace with your data source
    features = compute_features(df)
    print(features.tail())
