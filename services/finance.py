import yfinance as yf
from requests import Session
from settings import settings
from logger import app_log
from pandas import read_csv
import io, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
# from pytickersymbols import PyTickerSymbols



RESULT_LOCK = threading.Lock()

results = []

def fetch_available_symbols(limit: bool | int = False):
    try:
        with Session() as session:
            respnse = session.get(settings.YF_SYMBOLS_URL)
            respnse.raise_for_status()
            
            # stream csv file
            csv_data = read_csv(io.StringIO(respnse.text))
            
            symbols_name = "Symbol"
            if symbols_name in csv_data.columns:
                symbols: list = csv_data[symbols_name].tolist()
                return symbols if not limit else symbols[:limit]
            else:
                raise ValueError(f"Unable to locate `{symbols_name}` in csv_data")
            
    except Exception as e:
        app_log(title="FETCH_SYMBOLS_ERR", msg=e)


# Fetch stock data
def fetch_stocks_data():
    symbols = fetch_available_symbols(limit=300)
    app_log(title="INFO", msg=f"Symbols: {len(symbols):,}")
    
    
    # multi-thread stock data details
    with ThreadPoolExecutor() as executor:
        app_log(title="INFO", msg="Fetching data..")
        futures = [executor.submit(get_highest_volume_stocks_above_market_cap, symbol, i) for i, symbol in enumerate(symbols)]
        for future in as_completed(futures):
            pass
    
    return results
    
    
def get_highest_volume_stocks_above_market_cap(symbol: str, count: int):
    global results
    ticker = yf.Ticker(symbol)
    market_cap = float(ticker.info.get('marketCap', 0.0))
    try:
        if market_cap >= settings.MAX_VOLUME:
            history = ticker.history(period="max")
            highest_volume = float(history['Volume'].max())
            highest_volume_date = history['Volume'].idxmax().to_pydatetime().strftime("%m:%d:%Y-%H:%M:%S")
            with RESULT_LOCK:
                results.append([symbol, highest_volume, highest_volume_date])
                
            # app_log(title="FETCHED", msg=f"{symbol} [{count:,}]")
    except Exception as e:
        app_log(title=f"{symbol}_SYMBOL_ERR", msg=f"Error: {str(e)}")
    