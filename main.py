"""Plot a historical ticker example without modifying saved holdings."""
import argparse
from data_processing.stock_data import download_stock_data
from data_processing.indicators import calculate_indicators
from visualization.plot_stock import visualize_stock_data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--symbol', default='AAPL')
    parser.add_argument('--start', default='2024-01-01')
    parser.add_argument('--end', default='2024-12-31', help='Exclusive end date')
    args = parser.parse_args()
    data = download_stock_data(args.symbol, args.start, args.end)
    visualize_stock_data(calculate_indicators(data))


if __name__ == '__main__':
    main()
