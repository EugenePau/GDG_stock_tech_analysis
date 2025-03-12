import yfinance as yf
import config
from src.synthesizer import synthesisStock

def parse_from_yfinance():
    # Fetch stock data
    stock = yf.download(config.ticker_symbol, config.start_date, config.end_date)
    print(stock.isnull().sum())  # Check for missing data


    # Check if DataFrame is empty, else synthesis stock data
    if stock.empty:
        print("Error: Stock data fetch failed! DataFrame is empty.")
        print('Synthesis Stock Data...')
        stock = synthesisStock()
            
    else:
        print("Stock data fetched successfully!")
        stock.to_csv("AAPL_cached.csv") # data caching
        print("stock data cached!")
        
    return stock




