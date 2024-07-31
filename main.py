from services.finance import MarketCap



# fetch stock data 
obj = MarketCap()

obj.fetch_stocks_data()
# data = [['AAPL', 7421640800, '09:29:2000-00:00:00']]

# update_sheet_gspread(data=data)


# print()


# Automate trading and report generation
# trade()
# generate_report()