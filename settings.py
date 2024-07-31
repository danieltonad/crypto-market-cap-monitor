import os
from dotenv import load_dotenv
from logger import Logger

load_dotenv()

class Settings(Logger):
    YF_SYMBOLS_URL: str = os.getenv("YF_SYMBOLS_URL")
    GSHEET_PATH: str = os.getenv("GSHEET_PATH")
    MAX_VOLUME: int = 50_000_000_000
    
    