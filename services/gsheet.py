import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from settings import settings
from logger import app_log

SCOPES = ["https://googleapis.com/auth/spreadsheets"]


# Update Google Sheet
def update_google_sheet(data):
    credentials = None
    if os.path.exists(settings.GSHEET_PATH):
        credentials = Credentials.from_authorized_user_file(settings.GTOKEN_PATH, SCOPES)
    if not credentials or not credentials.valid():
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(settings.GSHEET_PATH, SCOPES)
            credentials = flow.run_local_server(port=0)
        with open(settings.GTOKEN_PATH, "w") as token:
            token.write(credentials.to_json())
            
    # auth checked?
    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadcheets()
        
        result = sheets.values().get(spreadsheetId=settings.GSHEET_ID, range="market_cap!A1:B1").execute()
    except Exception as err:
        app_log(title="Error", msg=str(err))
            
    # sheet.update('A1', [['Symbol', 'Highest Volume', 'Date']] + data)