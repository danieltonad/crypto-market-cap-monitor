import yfinance as yf
from requests import Session
from settings import settings
from logger import app_log
from pandas import read_csv
import io, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
# from pytickersymbols import PyTickerSymbols



MAX_VOLUME_50 = 50_000_000_000
MAX_VOLUME_20 = 20_000_000_000

RESULT_LOCK = threading.Lock()


results = []

def fetch_available_symbols(limit: bool | int = False):
    try:
        with Session() as session:
            respnse = session.get(settings.YF_SYMBOLS_URL)
            respnse.raise_for_status()
            
            # stream csv file
            csv_data = read_csv(io.StringIO(respnse.text))
            
            symbols_name = "Name"
            if symbols_name in csv_data.columns:
                symbols: list = csv_data[symbols_name].tolist() + ['AAPL']
                return symbols if not limit else symbols[:limit]
            else:
                raise ValueError(f"Unable to locate `{symbols_name}` in csv_data")
            
    except Exception as e:
        app_log(title="FETCH_SYMBOLS_ERR", msg=e)


# Fetch stock data
def fetch_stocks_data():
    symbols = fetch_available_symbols()
    app_log(title="INFO", msg=f"Symbols: {len(symbols):,}")
    # get_highest_volume_stocks_above_market_cap('AAPL')
    
    # multi-thread stock data details
    with ThreadPoolExecutor() as executor:
        app_log(title="INFO", msg="Fetching data..")
        futures = [executor.submit(get_highest_volume_stocks_above_market_cap, symbol) for symbol in symbols]
        app_log(title="INFO", msg="completely fetched data..")
    
    return results
    
    
def get_highest_volume_stocks_above_market_cap(symbol: str):
    global result
    ticker = yf.Ticker(symbol)
    market_cap = int(ticker.info.get('marketCap', 0))
    try:
        # print(f"{market_cap:,}")
        if market_cap >= MAX_VOLUME_50:
            history = ticker.history(period="max")
            highest_volume = history['Volume'].max().item()
            highest_volume_date = history['Volume'].idxmax().to_pydatetime().strftime("%m:%d:%Y-%H:%M:%S")
            with RESULT_LOCK:
                results.append([symbol, highest_volume, highest_volume_date])
        app_log(title="FETCHED", msg=f"{symbol} data")
    except Exception as e:
        app_log(title=f"{symbol}_SYMBOL_ERR", msg=f"Error: {str(e)}")
    