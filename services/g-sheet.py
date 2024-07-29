import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Update Google Sheet
def update_google_sheet(data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Stock Volume Tracker").sheet1
    sheet.clear()
    sheet.update('A1', [['Symbol', 'Current Volume', 'Highest Volume']] + data)