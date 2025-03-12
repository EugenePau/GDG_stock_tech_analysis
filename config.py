# config.py

# Trading Parameter
MA_parameter = ('EMA', 10, 30)  # 'EMA' or 'SMA', short window, long window 
RSI_parameter = (20, 30, 70, 80) # ex_oversold, oversold, overbought, ex_overbought
MACD_parameter = (12, 26, 9) # ema_short, ema_long, MACD_period
RSV_parameter = (12) # RSV_period

# Stock Infomration
ticker_symbol = 'AAPL'
start_date = "2023-01-01"
end_date = "2025-01-01"