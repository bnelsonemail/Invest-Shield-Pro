import yfinance as yf
import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt


# Sample Portfolio
portfolio = {
    'Assets': ['AAPL', 'MSFT', 'GOOGL', 'BTC-USD'],
    'Quantity': [10, 5, 8, 0.1]
}

df_portfolio = pd.DataFrame(portfolio)
print(df_portfolio)

# Fetch Real-time Data
def fetch_data(ticker):
    data = yf.download(ticker, period='1y', interval='1d')
    return data['Close']

def calculate_portfolio_value(portfolio):
    portfolio_value = 0
    for asset, quantity in zip(portfolio['Assets'], portfolio['Quantity']):
        price_data = fetch_data(asset)
        latest_price = price_data.iloc[-1]
        portfolio_value += latest_price * quantity
    return portfolio_value

portfolio_value = calculate_portfolio_value(df_portfolio)
print(f"Current Portfolio Value: ${portfolio_value:.2f}")


# # Risk Analysis
# def calculate_expected_return(prices):
#     log_returns = np.log(prices / prices.shift(1))
#     return log_returns.mean() * 252

# def calculate_risk(prices):
#     log_returns = np.log(prices / prices.shift(1))
#     return log_returns.std() * np.sqrt(252)

# # Visualization
# def plot_portfolio_value(asset, price_data):
#     plt.figure(figsize=(10, 6))
#     plt.plot(price_data.index, price_data, label=asset)
#     plt.title(f'{asset} Price Over Time')
#     plt.xlabel('Date')
#     plt.ylabel('Price')
#     plt.legend()
#     plt.show()

# # Example usage
# for asset in portfolio['Assets']:
#     data = fetch_data(asset)
#     plot_portfolio_value(asset, data)

#     print(f"Expected return for {asset}: {calculate_expected_return(data):.2f}")
#     print(f"Risk (volatility) for {asset}: {calculate_risk(data):.2f}")
