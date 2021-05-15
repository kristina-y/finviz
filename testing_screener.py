#Here, I will test the screener to make sure I can apply different filters

from finviz.screener import Screener

# Get dict of available filters
# filters dict contains the corresponding filter tags
filters = Screener.load_filter_dict()

# Welcome message:
print("Welcome to the program!")

# Determining investment timeframe (which will cause the algorithm to vary)
timeframe = input("What is your timeframe? Please enter 1, 2, or 3 depending on how many months you intend to hold: ")

# Data validation for timeframe
if timeframe == "1" or timeframe == "2" or timeframe == "3":
    print("Thank you. You have indicated that you plan to invest for ", timeframe, "months.")
else:
    print("That is not a valid input. We will proceed with a default value of 3 months.")
    timeframe = "3"
    
# Figuring out how much $ the user wishes to invest. This will determine the recommendation of how many investments to select
amount = input("How much money do you plan to invest? $")

#Data validation for amount
if float(amount) < 1000000000 and float(amount) > 0:
    print("You have entered that you wish to invest $", amount, ".")
    amount = float(amount)
else:
    print("Your entry is not valid. We will proceed with a default value of $1,000")
    amount = 1000

# Telling the user that data will be processed now.
print("We will now process your data and recommend a list of securities.")

# Determining proper filters based on the timeframe.
if timeframe == "1":
    some_filters = [filters["P/E"]["Low (<15)"], filters["Market Cap."]["Mid ($2bln to $10bln)"], filters["Target Price"]["30% Above Price"]]
    
elif timeframe == "2":

    some_filters = [filters["P/E"]["Low (<15)"], filters["Market Cap."]["Mid ($2bln to $10bln)"], filters["Target Price"]["30% Above Price"]]
elif timeframe == "3":

    some_filters = [filters["P/E"]["Low (<15)"], filters["Market Cap."]["Mid ($2bln to $10bln)"], filters["Target Price"]["30% Above Price"]]

else:
    print("Try again.")

stock_list = Screener(filters=some_filters, order="ticker")

# Creating a csv with the stock recommendations
print("Downloading csv file with the stock recommendations...")
stock_list.to_csv("test_stocks.csv")

# Stock_data is a list that will hold the recommendations.
print("Retrieving stock data...")
stock_data = stock_list.get_ticker_details()

#counter variable to determine how many options there are
counter = 0

# Printing out the tickers of the recommended equities.
print("We have processed the data and recommend the following securities:")
for i in stock_data:
    print(i["Ticker"])
    counter = counter + 1

# User may either proceed or quit the program
proceed = input("Please type 'Yes' if you wish to proceed. Type anything else if you would like to quit. ")

# User chose to proceed
if proceed == "Yes" or proceed == "yes":
    print("We will now run through each of the recommended stocks, and you may indicate if you would like to include it in your portfolio or not.")
    
    #Giving the user a recommendation for how many equities to invest in, if the amount is less than 1000.
    if (amount < 1000):
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