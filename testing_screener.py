#Here, I will test the screener to make sure I can apply different filters

from finviz.screener import Screener

# Get dict of available filters
# filters dict contains the corresponding filter tags
filters = Screener.load_filter_dict()


print("Welcome to the program!")

timeframe = input("What is your timeframe?")

if timeframe == "1":
    some_filters = [filters["P/E"]["Low (<15)"], filters["Market Cap."]["Mid ($2bln to $10bln)"], filters["Target Price"]["30% Above Price"]]
    stock_list = Screener(filters=some_filters, order="ticker")
    #print(stock_list)
    stock_list.to_csv("test_stocks.csv")

    print("Retrieving stock data...")
    stock_data = stock_list.get_ticker_details()
    #print(stock_data)

    print("We have processed the data and recommend the following securities:")
    for i in stock_data:
        print(i["Ticker"])

    proceed = input("Would you like to proceed? (Y/N)")


else:
    print("2")




#####
# Use raw filter tags in a list
# filters = ['geo_usa']
#filters = ["idx_sp500"]  # Shows companies in the S&P500
#print("Screening stocks...")
#stock_list = Screener(filters=filters, order="ticker")
#print(stock_list)



# Export the screener results to CSV file


# Create a SQLite database
# stock_list.to_sqlite("sp500.sqlite")