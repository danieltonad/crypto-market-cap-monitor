import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = ""
    YF_SYMBOLS_URL: str = os.getenv("YF_SYMBOLS_URL")
    
    
    
    
settings = Settings()
    