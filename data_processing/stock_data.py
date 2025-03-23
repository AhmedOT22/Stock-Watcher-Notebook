import yfinance as yf

def download_stock_data(symbol, start, end):
    """
    Download stock data from Yahoo Finance.

    Parameters:
        symbol (str): Stock ticker symbol (e.g., "AAPL").
        start (str): Start date in "YYYY-MM-DD" format.
        end (str): End date in "YYYY-MM-DD" format.

    Returns:
        pd.DataFrame: Stock data.
    """
    return yf.download(symbol, start=start, end=end)
