import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from settings import settings
from logger import app_log

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


# Update Google Sheet
def update_google_sheet(data):
    credentials = None
    if os.path.exists(settings.GTOKEN_PATH):
        credentials = Credentials.from_authorized_user_file(settings.GTOKEN_PATH, SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(settings.GSHEET_PATH, SCOPES)
            credentials = flow.run_local_server(port=5000)
            print(credentials)
        with open(settings.GTOKEN_PATH, "w") as token:
            token.write(credentials.to_json())
            
    # auth checked?
    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()
        
        result = sheets.values().get(spreadsheetId=settings.GSHEET_ID, range="market_cap!A1:B1").execute()
        
        values = result.get("values", [])
        
        for row in values:
            print(values)
            
            
    except HttpError as err:
        app_log(title="Http-Error", msg=str(err))
            
    except Exception as err:
        app_log(title="Error", msg=str(err))
      
    


def update_sheet_gspread(data):
    from gspread import service_account
    from pandas import DataFrame
    client = service_account(settings.GSHEET_PATH)
    sheet = client.open("MarketCap")
    worksheet = sheet.get_worksheet(0)
    worksheet.clear()
    worksheet.update(range_name="A1" ,values=[['Symbol', 'Highest Volume', 'Date']] + data)
    