#Here, I will test the screener to make sure I can apply different filters

from finviz.screener import Screener

# Get dict of available filters
# filters dict contains the corresponding filter tags
filters = Screener.load_filter_dict()


print("Welcome to the program!")

timeframe = input("What is your timeframe? Please enter 1, 2, or 3 depending on how many months you intend to hold: ")

if timeframe == "1" or timeframe == "2" or timeframe == "3":
    print("Thank you. You have indicated that you plan to invest for ", timeframe, "months.")
else:
    print("That is not a valid input. We will proceed with a default value of 3 months.")
    timeframe = "3"
    

amount = input("How much money do you plan to invest? $")


if timeframe == "1":
    some_filters = [filters["P/E"]["Low (<15)"], filters["Market Cap."]["Mid ($2bln to $10bln)"], filters["Target Price"]["30% Above Price"]]
    
elif timeframe == "2":

    some_filters = [filters["P/E"]["Low (<15)"], filters["Market Cap."]["Mid ($2bln to $10bln)"], filters["Target Price"]["30% Above Price"]]
elif timeframe == "3":

    some_filters = [filters["P/E"]["Low (<15)"], filters["Market Cap."]["Mid ($2bln to $10bln)"], filters["Target Price"]["30% Above Price"]]

else:
    print("Try again.")

stock_list = Screener(filters=some_filters, order="ticker")
#print(stock_list)
stock_list.to_csv("test_stocks.csv")

print("Retrieving stock data...")
stock_data = stock_list.get_ticker_details()
#print(stock_data)

#counter variable to determine how many options there are
counter = 0

print("We have processed the data and recommend the following securities:")
for i in stock_data:
    print(i["Ticker"])
    counter = counter + 1

proceed = input("Please type 'Yes' if you wish to proceed. Type 'No' if you would like to quit.")

if proceed == "Yes" or proceed == "yes":
    print("We will now run through each of the recommended stocks, and you may indicate if you would liske to include it in your portfolio or not.")
    print("Based on the amount of money that you are willing to invest, we would recommend selecting 5 of the ", counter, "recommended stocks/")

    #proceed with the program
else:
    print("Thank you for using the program. Goodbye.")


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