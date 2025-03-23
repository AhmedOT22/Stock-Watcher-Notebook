from data_processing.stock_data import download_stock_data
from data_processing.indicators import calculate_indicators
from visualization.plot_stock import visualize_stock_data
from models.watchlist import Watchlist
from models.portfolio import Portfolio

if __name__ == "__main__":
    # Download and process stock data
    data = download_stock_data("AAPL", "2024-01-01", "2024-12-31")
    data = calculate_indicators(data)
    visualize_stock_data(data)

    # Manage Watchlist
    watchlist = Watchlist()
    watchlist.add("AAPL")
    watchlist.visualize()

    # Manage Portfolio
    portfolio = Portfolio()
    portfolio.add("AAPL", 10)
    portfolio.visualize()
