import pandas as pd
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

import config

def plot_data(df):
    """
    Fetch stock data from yfinance and plot a K-line (candlestick) chart.

    Parameters:
    - ticker (str): Stock ticker symbol (e.g., "AAPL", "TSLA").
    - start (str): Start date (format: "YYYY-MM-DD").
    - end (str): End date (format: "YYYY-MM-DD").
    - interval (str): Data interval ("1d", "1h", "5m", etc.).
    """

    # Convert columns to numeric (force conversion in case of issues)
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows with missing values
    df.dropna(subset=["Open", "High", "Low", "Close"], inplace=True)

    # Plot K-line (candlestick chart)
    mpf.plot(df, type="candle", style="charles", title=f"K-Line Chart of {config.ticker_symbol}",
             ylabel="Price", volume=True, figsize=(10, 6), show_nontrading=True)

