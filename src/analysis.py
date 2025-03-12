import yfinance as yf
import pandas as pd
import pandas_ta as ta
import mplfinance as mpf
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

import config

def Strategy_MA(stock):

    ## MA based parameter
    indicator_type, short_window, long_window = config.MA_parameter
    ema_short = f"{indicator_type}_{short_window}"
    ema_long = f"{indicator_type}_{long_window}"
    
    stock[ema_short] = stock['Close'].ewm(span=short_window, adjust=False).mean()  # 10-day Exponential Moving Average
    stock[ema_long] = stock['Close'].ewm(span=long_window, adjust=False).mean()  # 30-day Exponential Moving Average

    stock['EMA_diff'] = stock[ema_short] - stock[ema_long]
    stock['EMA_rate_diff'] = stock[ema_short].diff() - stock[ema_long].diff()

    # Find Golden Cross (EMA_50 crosses above EMA_120)
    golden_crosses = (stock["EMA_diff"].shift(1) < 0) & (stock["EMA_diff"] > 0)

    # Find Death Cross (EMA_50 crosses below EMA_120)
    death_crosses = (stock["EMA_diff"].shift(1) > 0) & (stock["EMA_diff"] < 0)

    # Plot the EMAs
    plt.figure(figsize=(12,6))
    plt.plot(stock[ema_short], label = ema_short, color="blue", linewidth=2)
    plt.plot(stock[ema_long], label = ema_long, color="red", linewidth=2)

    # Highlight bullish regions where EMA_rate_diff > 0 ; bearish regions where EMA_rate_diff < 0 
    plt.fill_between(stock.index, stock[ema_short], stock[ema_long], 
                    where=(stock["EMA_rate_diff"] > 0), color="green", alpha=0.2)

    plt.fill_between(stock.index, stock[ema_short], stock[ema_long], 
                    where=(stock["EMA_rate_diff"] < 0), color="red", alpha=0.2)

    # Plot  Crosses 
    plt.scatter(stock.loc[golden_crosses].index, stock.loc[golden_crosses, ema_short], 
                color="green", marker="^", s=100, label="Golden Cross")

    plt.scatter(stock.loc[death_crosses].index, stock.loc[death_crosses, ema_short], 
                color="red", marker="v", s=100, label="Death Cross")

    # Labels and Legend
    plt.title("EMA Crossover with Highlighted Bullish Regions")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)

    # Show Plot
    plt.show()
    

def Strategy_MACD(stock):
    ## MACD ##

    short_window, long_window, signal = config.MACD_parameter
    ema_short = f"EMA_{short_window}"
    ema_long = f"EMA_{long_window}"
    
    # Construct EMA 
    stock[ema_short] = stock['Close'].ewm(span=short_window, adjust=False).mean() 
    stock[ema_long] = stock['Close'].ewm(span=long_window, adjust=False).mean() 
    
    # Compute DIFF
    stock['EMA_diff'] = stock[ema_short] - stock[ema_long]

    # Compute Signal DEA
    stock["Signal"] = stock['EMA_diff'].ewm(span=signal, adjust=False).mean()    # Signal Line (DEA)
    
    # Histogram, defined as DIFF - DEA
    stock["Histogram"] = stock['EMA_diff'] - stock["Signal"]  # Histogram

    # Plot MACD
    plt.figure(figsize=(12,6))

    # Plot MACD Line and Signal Line
    plt.plot(stock.index, stock['EMA_diff'], label="MACD Line", color="blue", linewidth=2)
    plt.plot(stock.index, stock["Signal"], label="Signal Line", color="red", linestyle="--", linewidth=2)

    # Plot Histogram (Bar Chart)
    plt.bar(stock.index, stock["Histogram"], color=np.where(stock["Histogram"] >= 0, "green", "red"), alpha=0.4)

    # Labels and Legend
    plt.title("MACD Indicator")
    plt.xlabel("Date")
    plt.ylabel("MACD Value")
    plt.axhline(y=0, color="black", linestyle="--", linewidth=1)  # Zero Line
    plt.legend()
    plt.grid(True)

    # Show Plot
    plt.show()

def Strategy_KD(stock):
    ## Stochastic Oscillator KD ## 

    # Calculation of Stochastic Oscillator (14-day period)
    period = config.RSV_parameter
    stock["Lowest Low"] = stock["Low"].rolling(window=period).min().fillna(stock["Low"].iloc[0])
    stock["Highest High"] = stock["High"].rolling(window=period).max().fillna(stock["High"].iloc[0])


    stock["RSV"] = ((stock["Close"].squeeze() - stock["Lowest Low"]) /          # stock['Close'] is a 1D dataframe while stock["Highest High"] and stock["Lowest Low"] is a Series, thus require the application of .squeeze()
                    (stock["Highest High"] - stock["Lowest Low"])) * 100


    stock["%K"] = stock["RSV"].rolling(window=3).mean()  # Standard %K (SMA)
    stock["%D"] = stock["%K"].rolling(window=3).mean()  # Standard %D (SMA)


    # Plot Stochastic Oscillator
    plt.figure(figsize=(12,6))
    plt.plot(stock.index, stock["RSV"], label="RSV (Raw Stochastic Value)", color="blue", linewidth=1)
    plt.plot(stock.index, stock["%K"], label="%K Line (Fast)", color="pink", linewidth=2)
    plt.plot(stock.index, stock["%D"], label="%D Line (Slow)", color="purple", linewidth=2)

    # Overbought & Oversold Levels
    plt.axhline(80, color="green", linestyle="--", alpha=0.5, label="Overbought (80)")
    plt.axhline(20, color="red", linestyle="--", alpha=0.5, label="Oversold (20)")

    # Labels & Legend
    plt.title("Stochastic Oscillator (RSV, %K, %D)")
    plt.xlabel("Date")
    plt.ylabel("Oscillator Value")
    plt.legend(loc="upper left")
    plt.grid(True)

    # Show Plot
    plt.show()

def Strategy_RSI(stock):
    ### RSI ###
    # Handle MultiIndex or flattened columns
    if isinstance(stock.columns, pd.MultiIndex):
        # Flatten MultiIndex if necessary
        stock.columns = ['_'.join(filter(None, col)) for col in stock.columns]

    # Access the Close column
    if 'Close_AAPL' in stock.columns:
        stock['Close'] = stock['Close_AAPL']  # Rename for simplicity
    elif 'Close' not in stock.columns:
        raise KeyError("Close column not found in the DataFrame!")

    # Drop rows with NaN values in the Close column
    stock = stock.dropna(subset=['Close'])

    # Compute RSI
    stock['RSI'] = ta.rsi(stock['Close'], length=14)

    # Drop NaN values in RSI (first few rows might be NaN due to calculation)
    stock = stock.dropna(subset=['RSI'])

    # Debugging: Ensure RSI is calculated
    print(stock[['Close', 'RSI']].tail())  # Print the last few rows for validation

    # RSI Strategy
    ex_oversold, oversold, overbought, ex_overbought = config.RSI_parameter

    # Identify Overbought & Oversold Regions
    overbought_regions = stock[stock["RSI"] > overbought].index
    oversold_regions = stock[stock["RSI"] < oversold].index
    extreme_overbought_regions = stock[stock["RSI"] > ex_overbought].index
    extreme_oversold_regions = stock[stock["RSI"] < ex_oversold].index

    # Plot RSI
    plt.figure(figsize=(12,6))
    plt.plot(stock.index, stock["RSI"], label="RSI", color="blue", linewidth=2)

    # Fill Extreme Overbought (RSI > 80)
    plt.fill_between(stock.index, ex_overbought, stock["RSI"], 
                    where=(stock["RSI"] > ex_overbought), 
                    color="darkred", alpha=0.3, label="Extreme Overbought")

    # Fill Overbought (70 < RSI < 80)
    plt.fill_between(stock.index, overbought, stock["RSI"], 
                    where=((stock["RSI"] > overbought) & (stock["RSI"] < ex_overbought)), 
                    color="orange", alpha=0.3, label="Overbought")

    # Fill Oversold (20 < RSI < 30)
    plt.fill_between(stock.index, stock["RSI"], oversold, 
                    where=((stock["RSI"] > ex_oversold) & (stock["RSI"] < oversold)), 
                    color="lightgreen", alpha=0.3, label="Oversold")

    # Fill Extreme Oversold (RSI < 20)
    plt.fill_between(stock.index, stock["RSI"], ex_oversold, 
                    where=(stock["RSI"] < ex_oversold), 
                    color="darkgreen", alpha=0.3, label="Extreme Oversold")


    # Plot thresholds
    plt.axhline(ex_overbought, color='red', linestyle='--', label='Overbought (80)')
    plt.axhline(overbought, color='orange', linestyle='--', label='Overbought (70)')
    plt.axhline(50, color="gray", linestyle="--", alpha=0.5)  # Neutral 50 line
    plt.axhline(oversold, color='lightgreen', linestyle='--', label='Oversold (30)')
    plt.axhline(ex_oversold, color='darkgreen', linestyle='--', label='Oversold (20)')



    plt.legend()
    plt.title("Relative Strength Index (RSI)")
    plt.xlabel("Date")
    plt.ylabel("RSI Value")
    plt.show()


def Strategy_SaR(stock):
    ### Support and Resistance ###

    # Ensure the DataFrame is flattened (if MultiIndex exists)
    if isinstance(stock.columns, pd.MultiIndex):
        stock.columns = ['_'.join(filter(None, col)) for col in stock.columns]

    # Calculate local minima and maxima
    n = 10  # Number of points to compare for local extrema
    stock['min'] = stock['Close'][argrelextrema(stock['Close'].values, np.less_equal, order=n)[0]]
    stock['max'] = stock['Close'][argrelextrema(stock['Close'].values, np.greater_equal, order=n)[0]]

    # Plot support and resistance

    plt.figure(figsize=(12, 6))
    plt.plot(stock['Close'], label="Close Price", alpha=0.5)
    plt.scatter(stock.index, stock['min'], label="Support", color='green', alpha=0.8)
    plt.scatter(stock.index, stock['max'], label="Resistance", color='red', alpha=0.8)
    plt.legend()
    plt.title("Support and Resistance Levels")
    plt.show()
