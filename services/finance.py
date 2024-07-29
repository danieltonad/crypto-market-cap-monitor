import yfinance as yf

# Fetch stock data
def fetch_stock_data():
    stocks = yf.Tickers('AAPL MSFT AMZN GOOGL FB')
    data = []
    for symbol in stocks.symbols:
        stock = stocks.tickers[symbol]
        hist = stock.history(period='max')
        max_volume = hist['Volume'].max()
        current_volume = hist['Volume'].iloc[-1]
        if current_volume > max_volume:
            data.append([symbol, current_volume, max_volume])
    return data