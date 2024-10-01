"""
    This script generates a fake investment portfolio using the Faker library.
    
    The portfolio includes:
    - Stocks: Randomly selected from a predefined list with random quantities and purchase prices.
    - Bonds: Randomly selected from a predefined list with random quantities and purchase prices.
    - T-notes: Randomly selected from a predefined list with random quantities and purchase prices.
    - Cryptocurrencies: Randomly selected from a predefined list with random quantities and purchase prices.
    
    The generated portfolio is printed to the console.
    
    Modules:
        faker: Used to generate fake data.
        random: Used to generate random selections and values.
    
    Attributes:
        stocks (list): Predefined list of stock symbols.
        bonds (list): Predefined list of bond symbols.
        t_notes (list): Predefined list of T-note symbols.
        cryptos (list): Predefined list of cryptocurrency symbols.
        portfolio (dict): Dictionary containing the generated investment portfolio.
"""
    
from faker import Faker
import random
import csv  # Import the csv module

fake = Faker()

# Define some fake stocks, bonds, T-notes, and cryptocurrencies
stocks = ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN', 'CEG', 'CORZ', 'NVDA', 'CVKD', 'UBER', 'ARE', 'MRNA', 'FMC', 'MMM', 'PFE', 'HUM', 'DG']
# bonds = ['US10Y', 'US30Y', 'CORP-AA-2028', 'CORP-BBB-2030', 'IBHI', 'JNK', 'BKLN', 'VCLT', 'EDV', 'BND', 'BRHYX', 'IBTG', 'BIL']
# t_notes = ['T-Note-5Y', 'T-Note-10Y']
cryptos = ['BTC', 'ETH', 'LTC', 'XRP']

# Generate a fake investment portfolio
portfolio = {
    "stocks": [
        {
            "symbol": random.choice(stocks),
            "quantity": random.randint(1, 100),
            "purchase_price": round(random.uniform(50, 5000), 2)
        } for _ in range(random.randint(3, 5))
    ],
    # "bonds": [
    #     {
    #         "symbol": random.choice(bonds),
    #         "quantity": random.randint(1, 50),
    #         "purchase_price": round(random.uniform(500, 20000), 2)
    #     } for _ in range(random.randint(2, 3))
    # ],
    # "t_notes": [
    #     {
    #         "symbol": random.choice(t_notes),
    #         "quantity": random.randint(1, 20),
    #         "purchase_price": round(random.uniform(1000, 10000), 2)
    #     } for _ in range(random.randint(1, 2))
    #],
    "cryptocurrencies": [
        {
            "symbol": random.choice(cryptos),
            "quantity": round(random.uniform(0.01, 5.0), 4),
            "purchase_price": round(random.uniform(100, 50000), 2)
        } for _ in range(random.randint(2, 3))
    ]
}

# Write the investment portfolio to a CSV file
with open('investment_portfolio.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write headers
    writer.writerow(['Asset Type', 'Symbol', 'Quantity', 'Purchase Price'])
    
    # Write stocks
    for stock in portfolio['stocks']:
        writer.writerow(['Stock', stock['symbol'], stock['quantity'], stock['purchase_price']])
    
    # # Write bonds
    # for bond in portfolio['bonds']:
    #     writer.writerow(['Bond', bond['symbol'], bond['quantity'], bond['purchase_price']])
    
    # # Write treasury notes
    # for t_note in portfolio['t_notes']:
    #     writer.writerow(['T-Note', t_note['symbol'], t_note['quantity'], t_note['purchase_price']])
    
    # Write cryptocurrencies
    for crypto in portfolio['cryptocurrencies']:
        writer.writerow(['Cryptocurrency', crypto['symbol'], crypto['quantity'], crypto['purchase_price']])

print("Fake investment portfolio has been written to 'investment_portfolio.csv'")
