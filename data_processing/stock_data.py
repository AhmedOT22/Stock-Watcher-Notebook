"""Download one ticker and normalize yfinance's optional MultiIndex columns."""
import pandas as pd
import yfinance as yf


def download_stock_data(symbol, start, end):
    symbol = str(symbol).strip().upper()
    if not symbol or pd.Timestamp(start) >= pd.Timestamp(end):
        raise ValueError('Supply a ticker and a start date before the exclusive end date.')
    data = yf.download(symbol, start=start, end=end, auto_adjust=True, progress=False)
    if data is None or data.empty:
        raise ValueError(f'No price observations returned for {symbol}.')
    if isinstance(data.columns, pd.MultiIndex):
        data = data.copy()
        data.columns = data.columns.get_level_values(0)
    if data.columns.has_duplicates or not {'Close', 'High', 'Low'}.issubset(data.columns):
        raise ValueError('Expected a single ticker with Close, High and Low prices.')
    return data
