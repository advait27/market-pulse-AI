# data_loader.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_mock_data(ticker: str = "AAPL", days: int = 60) -> pd.DataFrame:
    """
    Generate mock stock data for testing purposes.
    """
    dates = pd.date_range(end=datetime.today(), periods=days, freq='B')
    np.random.seed(42)
    price = np.cumsum(np.random.normal(loc=0.5, scale=2.0, size=days)) + 150
    high = price + np.random.normal(loc=1.5, scale=0.5, size=days)
    low = price - np.random.normal(loc=1.5, scale=0.5, size=days)
    open_ = price + np.random.normal(loc=0, scale=1.0, size=days)
    close = price + np.random.normal(loc=0, scale=1.0, size=days)
    volume = np.random.randint(int(1e6), int(5e6), size=days)

    df = pd.DataFrame({
        'Date': dates,
        'Open': open_,
        'High': high,
        'Low': low,
        'Close': close,
        'Volume': volume,
        'ticker': ticker
    })

    return df


if __name__ == "__main__":
    df = generate_mock_data()
    df.to_csv("mock_stock_data.csv", index=False)
    print(df.head())
