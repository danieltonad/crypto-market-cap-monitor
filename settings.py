import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    YF_SYMBOLS_URL: str = os.getenv("YF_SYMBOLS_URL")
    GSHEET_PATH: str = os.getenv("GSHEET_PATH")
    MAX_VOLUME: int = 50_000_000_000
    
settings = Settings()
    