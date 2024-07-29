from gspread import service_account
from settings import settings
from logger import app_log

def update_sheet_gspread(data):
    try:
        client = service_account(settings.GSHEET_PATH)
        sheet = client.open("MarketCap")
        worksheet = sheet.get_worksheet(0)
        worksheet.clear()
        worksheet.update(range_name="A1" ,values=[['Symbol', 'Highest Volume', 'Date']] + data)
        app_log(title="INFO", msg="Data Updated")
    except Exception as e:
        app_log(title="SHEET_ERR", msg=str(e))
    