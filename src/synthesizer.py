import numpy as np
import pandas as pd
import pandas_ta as ta
import config

def synthesisStock():
    # Generate date range for 3 years (business days only)
    date_range = pd.date_range(config.start_date, config.end_date, freq="B")  # 'B' means business days

    # Set random seed for reproducibility
    np.random.seed(42)

    # Initialize stock prices with a base value
    initial_price = 150  
    drift = 0.02  # Small positive drift to simulate market growth
    volatility = 2  # Higher value means more fluctuations

    # Generate synthetic stock prices using a random walk model
    open_prices = [initial_price]

    for _ in range(1, len(date_range)):
        # Next price = Prev price + Drift + Random noise
        next_price = open_prices[-1] + drift + np.random.normal(0, volatility)
        open_prices.append(round(next_price, 2))

    # Convert to numpy array
    open_prices = np.array(open_prices)

    # Generate High, Low, Close prices with short-term correlation
    high_prices = open_prices + np.round(np.random.uniform(0, 5, len(date_range)), 2)
    low_prices = open_prices - np.round(np.random.uniform(0, 5, len(date_range)), 2)
    close_prices = open_prices + np.round(np.random.normal(0, 1, len(date_range)), 2)  # Small noise for closing
    adj_close_prices = close_prices * np.random.uniform(0.99, 1.01, len(date_range))  # Small variation

    # Generate trading volumes with some short-term consistency
    volumes = np.random.randint(500000, 5000000, len(date_range))
    volumes = np.convolve(volumes, np.ones(5)/5, mode='same').astype(int)  # Smooth volume changes

    # Create DataFrame
    mock_stock_data = pd.DataFrame({
        "Date": date_range,
        "Open": open_prices,
        "High": high_prices,
        "Low": low_prices,
        "Close": close_prices,
        "Adj Close": adj_close_prices,
        "Volume": volumes
    })

    # Set Date as index
    mock_stock_data.set_index("Date", inplace=True)

    # Save to CSV (optional)
    mock_stock_data.to_csv("mock_stock_data.csv")
    return mock_stock_data
