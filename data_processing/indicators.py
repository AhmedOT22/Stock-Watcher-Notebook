import pandas as pd

def calculate_indicators(data):
    data['SMA_100'] = data['Close'].rolling(window=100).mean()
    data['EMA_100'] = data['Close'].ewm(span=100, adjust=False).mean()
    data['High-Low'] = data['High'] - data['Low']
    data['High-Close'] = abs(data['High'] - data['Close'].shift(1))
    data['Low-Close'] = abs(data['Low'] - data['Close'].shift(1))
    data['True_Range'] = data[['High-Low', 'High-Close', 'Low-Close']].max(axis=1)
    data['ATR'] = data['True_Range'].rolling(window=14).mean()
    data['Daily_Return'] = data['Close'].pct_change()
    return data
