from portfolio import Portfolio as pf
import matplotlib.pyplot as plt
import numpy as np



class RiskAnalysis:
    """
    A class to perform risk analysis on an investment portfolio.

    This class provides methods to evaluate various risk metrics of a given
    investment portfolio, such as volatility, beta, Sharpe ratio, and Value at 
    Risk (VaR). The portfolio must be passed in as a pandas DataFrame that 
    includes information such as the asset symbol, quantity, purchase price, 
    and current price.

    Attributes
    ----------
    portfolio : pandas.DataFrame
        A DataFrame representing the investment portfolio with columns such as 
        'Symbol', 'Quantity', 'Purchase Price', 'Current Price', and possibly 
        other metrics like historical returns and volatility.
    risk_free_rate : float, optional
        The risk-free rate to use in the calculation of risk-adjusted metrics 
        such as the Sharpe ratio. Default is 0.01 (1%).

    Methods
    -------
    calculate_volatility():
        Calculates the overall portfolio volatility based on individual asset 
        volatilities and their correlations.
    
    calculate_beta(market_returns):
        Computes the beta of the portfolio by comparing portfolio returns to 
        market returns.

    calculate_sharpe_ratio():
        Calculates the Sharpe ratio of the portfolio, a measure of risk-adjusted 
        return.

    calculate_var(confidence_level=0.95):
        Computes the Value at Risk (VaR) of the portfolio at a specified 
        confidence level.
    
    calculate_cvar(confidence_level=0.95):
        Computes the Conditional Value at Risk (CVaR), also known as Expected 
        Shortfall, for the portfolio at a specified confidence level.
    
    plot_risk_metrics():
        Produces a graphical representation of the risk metrics of the portfolio, 
        such as a risk-return scatter plot or VaR distributions.
    """
    
    def __init__(self, portfolio, risk_free_rate=0.01):
        """
        Initializes the RiskAnalysis class with the given portfolio.

        Parameters
        ----------
        portfolio : pandas.DataFrame
            A DataFrame representing the portfolio with columns such as 'Symbol',
            'Quantity', 'Purchase Price', 'Current Price', and others.
        risk_free_rate : float, optional
            The risk-free rate to use in the calculation of risk-adjusted metrics 
            such as the Sharpe ratio. Default is 0.01 (1%).
        """
        self.portfolio = portfolio
        self.risk_free_rate = risk_free_rate
    
    
    
    def plot_risk_return(self, risk_analysis, volatilities, returns, labels):
        """
        Generates a risk-return scatter plot for the portfolio.

        This method uses randomly generated returns and volatilities to demonstrate
        how to visually assess the trade-off between risk (volatility) and return.
        In practice, you should use actual portfolio returns and volatility data.

        Returns
        -------
        None
        """
        # Assuming Portfolio class provides method to get historical data and calculate risk
        for asset in pf.holdings:
            historical_data = pf.get_historical_data(asset['symbol'])
            expected_return = risk_analysis.calculate_expected_return(historical_data)
            volatility = risk_analysis.calculate_risk(historical_data)
            print(f"Asset: {asset['symbol']} | Expected Return: {expected_return:.2f} | Volatility: {volatility:.2f}")


        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.scatter(volatilities, returns, c='blue', label='Assets', s=100)
        
        # Annotate points
        for i, label in enumerate(labels):
            plt.annotate(label, (volatilities[i], returns[i]), fontsize=10)

        # Labels and title
        plt.title("Risk-Return Scatter Plot", fontsize=14)
        plt.xlabel("Volatility (Risk)", fontsize=12)
        plt.ylabel("Expected Return", fontsize=12)
        plt.grid(True)
        plt.show()

    def plot_var(self, confidence_level=0.95):
        """
        Plots the Value at Risk (VaR) distribution for the portfolio.

        VaR is a risk metric that estimates the maximum potential loss of a
        portfolio over a specific time horizon, given a certain confidence level.

        Parameters
        ----------
        confidence_level : float, optional
            The confidence level for VaR calculation. Default is 0.95 (95%).

        Returns
        -------
        None
        """
        # Simulate random returns for illustration
        np.random.seed(42)
        portfolio_returns = np.random.normal(0.01, 0.05, 1000)  # Mean = 1%, SD = 5%

        # Compute the VaR
        var_threshold = np.percentile(portfolio_returns, (1 - confidence_level) * 100)

        # Plot the distribution of portfolio returns
        plt.figure(figsize=(10, 6))
        plt.hist(portfolio_returns, bins=50, color='skyblue', alpha=0.7)
        
        # Highlight VaR region
        plt.axvline(var_threshold, color='red', linestyle='dashed', linewidth=2)
        plt.text(var_threshold, 30, f'VaR at {confidence_level*100}%: {var_threshold:.4f}',
                 color='red', fontsize=12, verticalalignment='center')
        
        plt.title(f"Portfolio Return Distribution with VaR ({confidence_level*100:.0f}%)",
                  fontsize=14)
        plt.xlabel("Portfolio Return", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.grid(True)
        plt.show()
    
    def calculate_volatility(self, symbol):
        """
        Calculates the volatility of an asset based on historical price data.
        
        Volatility is the standard deviation of the log returns of the asset.
        
        Parameters
        ----------
        symbol : str
            The symbol of the asset for which to calculate volatility.
        
        Returns
        -------
        float
            The volatility of the asset (annualized).
        """
        # Get historical data for the symbol using the Portfolio class
        historical_data = self.portfolio.get_historical_data(symbol)

        if historical_data is not None:
            # Calculate daily log returns
            historical_data['Log Return'] = np.log(historical_data['Close'] / historical_data['Close'].shift(1))
            volatility = historical_data['Log Return'].std() * np.sqrt(252)  # Annualize volatility
            return volatility
        else:
            print(f"Failed to calculate volatility for {symbol}")
            return None

    def calculate_beta(self, market_returns):
        """
        Calculates the beta of the portfolio.

        Beta measures the sensitivity of the portfolio’s returns relative to the 
        overall market. A beta of 1 means the portfolio moves with the market, 
        while a beta higher than 1 means it is more volatile than the market.

        Parameters
        ----------
        market_returns : pandas.Series
            A Series of historical market returns for comparison.

        Returns
        -------
        float
            The beta of the portfolio.
        """
        pass
    
    def calculate_sharpe_ratio(self, symbol):
        """
        Calculates the Sharpe ratio of an asset based on historical data.
        
        Sharpe ratio is a measure of risk-adjusted return.
        
        Parameters
        ----------
        symbol : str
            The symbol of the asset for which to calculate the Sharpe ratio.
        
        Returns
        -------
        float
            The Sharpe ratio of the asset.
        """
        historical_data = self.portfolio.get_historical_data(symbol)

        if historical_data is not None:
            # Calculate daily log returns
            historical_data['Log Return'] = np.log(historical_data['Close'] / historical_data['Close'].shift(1))

            # Calculate annualized return and volatility
            annualized_return = historical_data['Log Return'].mean() * 252
            annualized_volatility = historical_data['Log Return'].std() * np.sqrt(252)

            # Calculate Sharpe ratio
            sharpe_ratio = (annualized_return - self.risk_free_rate) / annualized_volatility
            return sharpe_ratio
        else:
            print(f"Failed to calculate Sharpe ratio for {symbol}")
            return None
    
    def calculate_var(self, confidence_level=0.95):
        """
        Calculates the Value at Risk (VaR) of the portfolio.

        VaR estimates the maximum expected loss of the portfolio over a given 
        time horizon at a specific confidence level. This method uses historical 
        returns to compute VaR.

        Parameters
        ----------
        confidence_level : float, optional
            The confidence level for VaR calculation. Default is 0.95 (95%).

        Returns
        -------
        float
            The estimated Value at Risk (VaR) for the portfolio.
        """
        pass
    
    def calculate_cvar(self, confidence_level=0.95):
        """
        Calculates the Conditional Value at Risk (CVaR) or Expected Shortfall.

        CVaR provides an estimate of the expected loss of the portfolio, given 
        that a loss greater than VaR has occurred. It is more conservative than 
        VaR and focuses on the tail risk.

        Parameters
        ----------
        confidence_level : float, optional
            The confidence level for CVaR calculation. Default is 0.95 (95%).

        Returns
        -------
        float
            The estimated Conditional Value at Risk (CVaR) for the portfolio.
        """
        pass
    
    def plot_risk_metrics(self):
        """
        Generates a visual representation of the portfolio's risk metrics.

        This method can create various plots such as a risk-return scatter plot,
        VaR distribution, or rolling volatility to provide a visual insight into 
        the portfolio’s risk characteristics.

        Returns
        -------
        None
        """
        pass

    # Risk Analysis
    def calculate_expected_return(self, prices):
        log_returns = np.log(prices / prices.shift(1))
        return log_returns.mean() * 252

    def calculate_risk(self, prices):
        log_returns = np.log(prices / prices.shift(1))
        return log_returns.std() * np.sqrt(252)

    # Visualization
    def plot_portfolio_value(self, asset, price_data):
        plt.figure(figsize=(10, 6))
        plt.plot(price_data.index, price_data, label=asset)
        plt.title(f'{asset} Price Over Time')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

# Example usage
for asset in portfolio['Assets']:
    data = fetch_data(asset)
    plot_portfolio_value(asset, data)
    print(f"Expected return for {asset}: {calculate_expected_return(data):.2f}")
    print(f"Risk (volatility) for {asset}: {calculate_risk(data):.2f}")
