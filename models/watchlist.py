import json
import os
import time
import yfinance as yf
import matplotlib.pyplot as plt

class Watchlist:
    def __init__(self, filename="watchlist.json"):
        self.filename = filename
        self.watchlist = self._load_watchlist()

    def _load_watchlist(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []

    def _save_watchlist(self):
        with open(self.filename, 'w') as file:
            json.dump(self.watchlist, file)

    def add(self, symbol):
        symbol = symbol.upper()
        if symbol not in self.watchlist:
            self.watchlist.append(symbol)
            self._save_watchlist()

    def remove(self, symbol):
        symbol = symbol.upper()
        if symbol in self.watchlist:
            self.watchlist.remove(symbol)
            self._save_watchlist()

    def view(self):
        return self.watchlist

    def fetch_data(self, symbol):
        stock = yf.Ticker(symbol)
        return stock.history(period="1d", interval="1m")

    def visualize(self):
        symbols = self.view()
        plt.figure(figsize=(14, 8))
        for symbol in symbols:
            data = self.fetch_data(symbol)
            if data is not None:
                plt.plot(data.index, data['Close'], label=f'{symbol} Real-Time Price')
                time.sleep(1)
        plt.xlabel('Time')
        plt.ylabel('Price (USD)')
        plt.title('Real-Time Stock Prices for the Watchlist')
        plt.legend()
        plt.grid()
        plt.show()
