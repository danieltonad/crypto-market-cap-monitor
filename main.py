from fastapi import FastAPI
from settings import settings


app = FastAPI(title=settings.APP_NAME)


@app.get('/')
async def root():
    from services.finance import fetch_stocks_data
    from services.gsheet import update_sheet_gspread
    
    update_sheet_gspread(data=['AAPL', 7421640800, '09:29:2000-00:00:00'])
    
    return ""