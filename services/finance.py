import yfinance as yf
from requests import Session
from settings import settings
from logger import app_log
from pandas import read_csv
import io

MAX_VOLUME = 50_000_000_000

def fetch_available_symbols(limit: bool | int = False):
    try:
        with Session() as session:
            respnse = session.get(settings.YF_SYMBOLS_URL)
            respnse.raise_for_status()
            
            # stream csv file
            csv_data = read_csv(io.StringIO(respnse.text))
            
            symbols_name = "Name"
            if symbols_name in csv_data.columns:
                symbols: list = csv_data[symbols_name].tolist()
                return " ".join(symbols) if not limit else " ".join(symbols[:limit])
            else:
                raise ValueError(f"Unable to locate `{symbols_name}` in csv_data")
            
    except Exception as e:
        app_log(msg="FETCH_SYMBOLS_ERR", error=e)
    

# Fetch stock data
def fetch_stock_data():
    symbols = fetch_available_symbols(limit=5)
    stocks = yf.Tickers(symbols)
    stocks.download()
    data = []
    for symbol in stocks.symbols:
        stock = stocks.tickers[symbol]
        # print(stock.get('sharesOutstanding'))
        history = stock.history(period='max')
        return history
        # max_volume = history['Volume'].max()
        # data.append(max_volume)
    #     current_volume = hist['Volume'].iloc[-1]
    #     if current_volume > max_volume:
    #         data.append([symbol, current_volume, max_volume])
    # data.append([symbol, current_volume, max_volume])
    return data