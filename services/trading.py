# Required Libraries
import ccxt
import pandas as pd

# Set up CCXT with Coinbase
exchange = ccxt.coinbasepro({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
    'password': 'YOUR_PASSWORD',
})

# Trading strategy example (simplified)
def trade():
    balance = exchange.fetch_balance()
    ticker = exchange.fetch_ticker('BTC/USD')
    price = ticker['last']
    
    # Example strategy: Buy if balance allows, sell if we have BTC
    if balance['USD']['free'] > price:
        order = exchange.create_market_buy_order('BTC/USD', 1)
    elif balance['BTC']['free'] > 0:
        order = exchange.create_market_sell_order('BTC/USD', 1)
    return order

# Generate profit/loss report
def generate_report():
    trades = exchange.fetch_my_trades('BTC/USD')
    df = pd.DataFrame(trades)
    df['profit_loss'] = df['price'] * df['amount']
    df.to_csv('crypto_trading_report.csv')

# Automate trading and report generation
trade()
generate_report()
