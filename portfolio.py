import yfinance as yf
import pandas as pd

# Read the CSV file into a pandas DataFrame
df_portfolio = pd.read_csv('investment_portfolio.csv')

# Display the loaded portfolio
print("Portfolio loaded from CSV:\n", df_portfolio)


class Portfolio:
    """
    A class to represent a financial portfolio.

    Attributes
    ----------
    holdings : list
        A list of dictionaries where each dictionary represents an investment
        with keys 'symbol', 'quantity', and 'purchase_price'.
    total_value : float
        The total value of the portfolio.
    """

    def __init__(self, holdings=None):
        """
        Initialize the Portfolio.

        Parameters
        ----------
        holdings : list of dict, optional
            A list of holdings. Each holding is represented as a dictionary
            with keys 'symbol', 'quantity', and 'purchase_price'.
        """
        if holdings is None:
            holdings = []
        
        self.holdings = holdings
        self.total_value = 0.0

    def __str__(self):
        """
        Return a string representation of the portfolio.

        Returns
        -------
        str
            A string showing each holding's symbol, quantity, and purchase price.
        """
        portfolio_str = "Portfolio:\n"
        for holding in self.holdings:
            portfolio_str += (
                f"{holding['symbol']} - Quantity: {holding['quantity']}, "
                f"Purchase Price: {holding['purchase_price']}\n"
            )
        return portfolio_str
        
    def fetch_data(self, ticker):
        """
        Fetch real-time stock data for a given ticker symbol using yfinance.

        Parameters
        ----------
        ticker : str
            The symbol of the stock (e.g., 'AAPL', 'TSLA', 'BTC-USD').

        Returns
        -------
        pandas.Series
            A Series containing the historical closing prices of the stock.
        """
        data = yf.download(ticker, period='ytd', interval='1d')
        self.data = data
        return data['Close']

    def calculate_portfolio_value(self, df):
        """
        Calculate the portfolio value based on real-time stock data.

        This method updates the DataFrame with the current price, current value,
        and gain/loss for each investment.

        Parameters
        ----------
        df : pandas.DataFrame
            The DataFrame representing the portfolio, containing columns
            'Symbol', 'Quantity', and 'Purchase Price'.

        Returns
        -------
        tuple
            A tuple containing the updated total portfolio value and the updated
            DataFrame with 'Current Price', 'Current Value', and 'Gain/Loss'.
        """
        portfolio_value = 0
        portfolio_investment = 0
        
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
                price_data = self.fetch_data(symbol)
                latest_price = price_data.iloc[-1]  # Get the latest closing price

                # Update the DataFrame with the latest prices and calculations
                df.at[idx, 'Current Price'] = latest_price
                df.at[idx, 'Current Value'] = latest_price * quantity
                df.at[idx, 'Gain/Loss'] = (
                    (latest_price - purchase_price) * quantity
                )

                # Accumulate the total portfolio value
                portfolio_value += latest_price * quantity
                
                # Total loss/gain of portfolio based on current value
                portfolio_investment += purchase_price * quantity
                portfolio_performance = portfolio_value - portfolio_investment
                

            except Exception as e:
                print(f"Failed to fetch data for {symbol}: {e}")
        
        return portfolio_value, portfolio_performance, df
    
    def get_historical_data(self, ticker, period='1y'):
        """
        Fetches historical data for a given asset (symbol) over a specified period.
        
        Parameters
        ----------
        ticker : str
            The symbol of the asset (e.g., 'AAPL', 'TSLA', 'BTC-USD').
        period : str, optional
            The period over which to fetch historical data (default is 1 year).
            Acceptable values: '1d', '5d', '1mo', '3mo', '6mo', '1y', '5y', 'max'.
        
        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the historical data (Date, Open, High, Low, Close).
        """
        try:
            historical_data = yf.download(ticker, period=period)
            return historical_data
        except Exception as e:
            print(f"Failed to fetch historical data for {ticker}: {e}")
            return None


# Create a Portfolio instance
portfolio = Portfolio()

# Call calculate_portfolio_value to get the updated portfolio value and performance
portfolio_value, portfolio_performance, df_portfolio = portfolio.calculate_portfolio_value(df_portfolio)

# Print updated portfolio details with current prices and gain/loss
print("\nPortfolio Details with Current Prices and Gain/Loss:\n", df_portfolio)

# Print total portfolio value
print(f"\nCurrent Portfolio Value: ${portfolio_value:.2f}")

# Print total portfolio performance with formatting
if portfolio_performance < 0:
    # Negative: use parentheses and red color
    print(f"\033[91mCurrent Portfolio Performance: "
          f"(${abs(portfolio_performance):.2f})\033[0m")
else:
    # Positive: normal display
    print(f"\nCurrent Portfolio Performance: ${portfolio_performance:.2f}")



