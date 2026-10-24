import math
from config import PORTFOLIO_FILE
from utils.file_manager import load_json, save_json
import json
import os
import yfinance as yf
import matplotlib.pyplot as plt

class Portfolio:
    def __init__(self, filename=PORTFOLIO_FILE):
        self.filename = filename
        self.portfolio = self._load_portfolio()

    def _load_portfolio(self):
        value = load_json(self.filename, {})
        if not isinstance(value, dict):
            raise ValueError("Invalid portfolio JSON structure.")
        return value

    def _save_portfolio(self):
        save_json(self.filename, self.portfolio)

    def add(self, symbol, shares):
        if isinstance(shares, bool) or not isinstance(shares, (int, float)) or not math.isfinite(shares) or shares <= 0:
            raise ValueError("Shares must be a finite positive number.")
        symbol = str(symbol).strip().upper()
        if not symbol:
            raise ValueError("Stock symbol cannot be empty.")
        self.portfolio[symbol] = self.portfolio.get(symbol, 0) + shares
        self._save_portfolio()

    def remove(self, symbol):
        if symbol.upper() in self.portfolio:
            del self.portfolio[symbol.upper()]
            self._save_portfolio()

    def view(self):
        return self.portfolio.copy()

    def fetch_stock_prices(self):
        prices = {}
        for symbol in self.portfolio:
            try:
                stock = yf.Ticker(symbol)
                price = stock.history(period="1d")["Close"].iloc[-1]
                prices[symbol] = float(price) 
            except Exception as e:
                print(f"Error fetching price for {symbol}: {e}")
                prices[symbol] = None  # Handle missing data gracefully
        return prices
        
    def visualize(self):
        stock_prices = self.fetch_stock_prices()
        worth_per_stock = {}
    
        for symbol, shares in self.portfolio.items():
            price = stock_prices.get(symbol)
            if price is not None:
                try:
                    worth_per_stock[symbol] = float(price) * shares
                except ValueError:
                    print(f"Skipping {symbol} due to invalid price data.")
    
        total_worth = sum(worth_per_stock.values())
    
        if not worth_per_stock or total_worth <= 0:
            print("No valid stock price data available for visualization.")
            return
    
        plt.figure(figsize=(8, 8))
        plt.pie(
            worth_per_stock.values(), labels=worth_per_stock.keys(),
            autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors
        )
        plt.title(f'Portfolio Allocation\n(Total Value: ${total_worth:,.2f})')
        plt.axis('equal')
        plt.show()
