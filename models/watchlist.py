from config import WATCHLIST_FILE
from utils.file_manager import load_json, save_json
import json
import os
import time
import yfinance as yf
import matplotlib.pyplot as plt

class Watchlist:
    def __init__(self, filename=WATCHLIST_FILE):
        self.filename = filename
        self.watchlist = self._load_watchlist()

    def _load_watchlist(self):
        value = load_json(self.filename, [])
        if not isinstance(value, list):
            raise ValueError("Invalid watchlist JSON structure.")
        return value

    def _save_watchlist(self):
        save_json(self.filename, self.watchlist)

    def add(self, symbol):
        symbol = str(symbol).strip().upper()
        if not symbol:
            raise ValueError("Stock symbol cannot be empty.")
        if symbol not in self.watchlist:
            self.watchlist.append(symbol)
            self._save_watchlist()

    def remove(self, symbol):
        symbol = str(symbol).strip().upper()
        if not symbol:
            raise ValueError("Stock symbol cannot be empty.")
        if symbol in self.watchlist:
            self.watchlist.remove(symbol)
            self._save_watchlist()

    def view(self):
        return self.watchlist.copy()

    def fetch_data(self, symbol):
        stock = yf.Ticker(symbol)
        return stock.history(period="1d", interval="1m")

    def visualize(self):
        symbols = self.view()
        plt.figure(figsize=(14, 8))
        for symbol in symbols:
            data = self.fetch_data(symbol)
            if data is not None and not data.empty:
                plt.plot(data.index, data['Close'], label=f'{symbol} Latest Price')
                time.sleep(1)
        plt.xlabel('Time')
        plt.ylabel('Price (quote currency)')
        plt.title('Latest Retrieved Stock Prices for the Watchlist')
        plt.legend()
        plt.grid()
        plt.show()
