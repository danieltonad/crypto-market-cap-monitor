import yfinance as yf
from requests import Session
from settings import Settings
from pandas import read_csv
import io, threading
from gspread import service_account
from concurrent.futures import ThreadPoolExecutor, as_completed



class MarketCap(Settings):
    result_lock  = None
    results: list
    count: int
    total: int
    
    def __init__(self) -> None:
        self.result_lock = threading.Lock()
        self.results = []
        self.count = 0
        self.total = 0

    def __fetch_available_symbols(self, limit: bool | int = False):
        try:
            with Session() as session:
                respnse = session.get(self.YF_SYMBOLS_URL)
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
            self.app_log(title="FETCH_SYMBOLS_ERR", msg=e)


    # Fetch stock data
    def fetch_stocks_data(self) -> list:
        symbols = self.__fetch_available_symbols(limit=300)
        self.total = len(symbols)
        self.app_log(title="INFO", msg=f"Symbols: {self.total:,}")
        
        # multi-thread stock data details
        with ThreadPoolExecutor() as executor:
            self.app_log(title="INFO", msg="Fetching data..")
            futures = [executor.submit(self.__get_highest_volume_stocks_above_market_cap, symbol) for symbol in symbols]
                    
        self.app_log(title="INFO", msg="completely fetched data..")
        
        # update goole shit
        self.__update_sheet()
        
        return self.results
    
    
    def __get_highest_volume_stocks_above_market_cap(self, symbol: str):
        self.count += 1
        ticker = yf.Ticker(symbol)
        market_cap = float(ticker.info.get('marketCap', 0.0))
        try:
            if market_cap >= self.MAX_VOLUME:
                history = ticker.history(period="max")
                highest_volume = float(history['Volume'].max())
                highest_volume_date = history['Volume'].idxmax().to_pydatetime().strftime("%m:%d:%Y-%H:%M:%S")
                with self.result_lock:
                    self.results.append([symbol, highest_volume, highest_volume_date])
            
            print(f"Fetching data | {self.count:,}/{self.total:,}", end="\r")        
        except Exception as e:
            self.app_log(title=f"{symbol}_SYMBOL_ERR", msg=f"Error: {str(e)}")
            
    
    def __update_sheet(self):
        client = service_account(self.GSHEET_PATH)
        sheet = client.open("MarketCap")
        worksheet = sheet.get_worksheet(0)
        worksheet.clear()
        worksheet.update(range_name="A1" ,values=[['Symbol', 'Highest Volume', 'Date']] + self.results)
    