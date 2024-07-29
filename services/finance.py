import yfinance as yf
from requests import Session
from settings import settings
from logger import app_log
from pandas import read_csv, DataFrame
import ast, threading
from concurrent.futures import ThreadPoolExecutor, as_completed


MAX_VOLUME_50 = 50_000_000_000
MAX_VOLUME_20 = 20_000_000_000
RESULT_LOCK = threading.Lock()


results = []

def fetch_available_tickers(limit: bool | int = False):
    try:
        with Session() as session:
            respnse = session.get(settings.YF_SYMBOLS_URL)
            respnse.raise_for_status()
            
            
            # stream csv file
            data = ast.literal_eval(respnse.text)
            print(data)
            # Convert the data to a DataFrame
            df = DataFrame(data, columns=['ticker', 'date', 'currency_code', 'free_cash_flow', 'total_assets', 'market_cap', 'total_revenue', 'validity'])
            # Extract all tickers
            tickers = df['ticker'].tolist()
            return tickers if not limit else tickers[:limit]
            
    except Exception as e:
        app_log(title="FETCH_SYMBOLS_ERR", msg=e)
    

# Fetch stock data
def fetch_stocks_data():
    symbols = fetch_available_tickers()
    app_log(title="INFO", msg=f"Symbols: {len(symbols):,}")
    
    # multi-thread stock data details search
    # with ThreadPoolExecutor() as executor:
    #     futures = [executor.submit(get_highest_volume_stocks_above_market_cap, symbol) for symbol in symbols]
    #     app_log(title="INFO", msg="Fetching data..")
        
    #     for future in as_completed(futures):
    #         pass
        
    #     app_log(title="INFO", msg="completely fetched data..")
    
    return results
        
    # get_highest_volume_stocks_above_market_cap('AAPL')
    
    
def get_highest_volume_stocks_above_market_cap(symbol: str):
    global result
    ticker = yf.Ticker(symbol)
    market_cap = int(ticker.info.get('marketCap', 0))
    try:
        if market_cap >= MAX_VOLUME_50:
            history = ticker.history(period="max")
            highest_volume = history['Volume'].max()
            highest_volume_date = history['Volume'].idxmax().to_pydatetime().strftime("%m:%d:%Y-%H:%M:%S")
            with RESULT_LOCK:
                result.append([symbol, highest_volume, highest_volume_date])
        app_log(title="FETCHED", msg=f"{symbol} data")
    except Exception as e:
        app_log(msg=f"{symbol}_SYMBOL_ERR", error=f"Error: {str(e)}")
    