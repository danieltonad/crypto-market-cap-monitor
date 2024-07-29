from services.finance import fetch_stocks_data
from services.gsheet import update_google_sheet


update_google_sheet(data=['AAPL', 7421640800, '09:29:2000-00:00:00'])


# print(fetch_stocks_data())


# Automate trading and report generation
# trade()
# generate_report()