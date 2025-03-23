import json
import os
import yfinance as yf
import matplotlib.pyplot as plt

class Portfolio:
    def __init__(self, filename="portfolio.json"):
        self.filename = filename
        self.portfolio = self._load_portfolio()

    def _load_portfolio(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return {}

    def _save_portfolio(self):
        with open(self.filename, 'w') as file:
            json.dump(self.portfolio, file)

    def add(self, symbol, shares):
        symbol = symbol.upper()
        self.portfolio[symbol] = self.portfolio.get(symbol, 0) + shares
        self._save_portfolio()

    def remove(self, symbol):
        if symbol.upper() in self.portfolio:
            del self.portfolio[symbol.upper()]
            self._save_portfolio()

    def view(self):
        return self.portfolio

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
    
        if not worth_per_stock:
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
