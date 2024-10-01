import yfinance as yf
import pandas as pd

# Read the CSV file into a pandas DataFrame
df_portfolio = pd.read_csv('investment_portfolio.csv')

# Display the loaded portfolio
print("Portfolio loaded from CSV:\n", df_portfolio)

# Fetch real-time data for a given ticker symbol
def fetch_data(ticker):
    data = yf.download(ticker, period='ytd', interval='1d')
    return data['Close']

# Calculate and print the details of each investment
def calculate_portfolio_value(df):
    portfolio_value = 0
    
    # Add columns for current unit price, current value, and gain/loss
    df['Current Price'] = 0.0
    df['Current Value'] = 0.0
    df['Gain/Loss'] = 0.0

    for idx, row in df.iterrows():
        symbol = row['Symbol']
        quantity = row['Quantity']
        purchase_price = row['Purchase Price']
        
        # Fetch the latest price data for the symbol
        try:
            price_data = fetch_data(symbol)
            latest_price = price_data.iloc[-1]  # Get the latest closing price

            # Update the DataFrame with the latest prices and calculations
            df.at[idx, 'Current Price'] = latest_price
            df.at[idx, 'Current Value'] = latest_price * quantity
            df.at[idx, 'Gain/Loss'] = (latest_price - purchase_price) * quantity

            # Accumulate the total portfolio value
            portfolio_value += latest_price * quantity

        except Exception as e:
            print(f"Failed to fetch data for {symbol}: {e}")
    
    return portfolio_value, df

# Calculate and print the portfolio value and gain/loss details
portfolio_value, df_portfolio = calculate_portfolio_value(df_portfolio)
print("\nPortfolio Details with Current Prices and Gain/Loss:\n", df_portfolio)

# Print total portfolio value
print(f"\nCurrent Portfolio Value: ${portfolio_value:.2f}")



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
