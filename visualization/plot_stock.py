import matplotlib.pyplot as plt

def visualize_stock_data(data):
    plt.figure(figsize=(8,10))

    plt.subplot(2, 1, 1)
    plt.plot(data.index, data['Close'], label='Close Price', color='blue')
    plt.plot(data.index, data['SMA_100'], label='SMA 100', linestyle='--', color='orange')
    plt.plot(data.index, data['EMA_100'], label='EMA 100', linestyle='-', color='green')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title('Closing Price')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(data.index, data['ATR'], label='ATR', color='red', linestyle='-')
    plt.plot(data.index, data['Daily_Return'], label='Daily Return', color='purple', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('ATR and Daily Return')
    plt.legend()

    plt.tight_layout()
    plt.show()
