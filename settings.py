import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = "Market_Cap_monitor"
    YF_SYMBOLS_URL: str = os.getenv("YF_SYMBOLS_URL")
    GSHEET_PATH: str = os.getenv("GSHEET_PATH")
    GSHEET_ID: str = os.getenv("GSHEET_ID")
    GTOKEN_PATH: str = "token.json"
    

    
settings = Settings()
    