import matplotlib.pyplot as plt

def visualize_portfolio(stock_prices, portfolio):
    """
    Visualizes the portfolio allocation based on stock values.

    Parameters:
        stock_prices (dict): Dictionary with stock symbols as keys and latest prices as values.
        portfolio (dict): Dictionary with stock symbols as keys and number of shares as values.
    """
    worth_per_stock = {symbol: stock_prices[symbol] * shares 
                       for symbol, shares in portfolio.items() if symbol in stock_prices}
    
    total_worth = sum(worth_per_stock.values())

    if not worth_per_stock:
        print("No valid stock price data available for visualization.")
        return

    plt.figure(figsize=(8, 8))
    plt.pie(worth_per_stock.values(), labels=worth_per_stock.keys(), 
            autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
    plt.title(f'Portfolio Allocation\n(Total Value: ${total_worth:,.2f})')
    plt.axis('equal')
    plt.show()
