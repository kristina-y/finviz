#Here is my program:

# Defining a function.
# This will be necessary later on
def negative_sharpe(weights):
    weights = np.array(weights)
    pret = np.dot(weights, mu)
    pvol = np.sqrt(np.dot(weights,np.dot(VarCov, weights.T)))
    return -(pret-rf)/pvol

from finviz.screener import Screener

# Get dict of available filters
# filters dict contains the corresponding filter tags
filters = Screener.load_filter_dict()

# Welcome message:
print("Welcome to the program! Today, we will help you make an investment plan.")

print("First, what is your investment timeframe? Your three choices are as follows:")
print("    1. I plan to hold my investments for under 3 months")
print("    2. I plan to hold my investments for 3-12 months.")
print("    3. I plan to hold my investments for over 1  year.")

# Determining investment timeframe (which will cause the algorithm to vary)
timeframe = input("Please enter 1, 2, or 3 depending on how many months you intend to hold: ")

# Data validation for timeframe
if timeframe == "1" or timeframe == "2" or timeframe == "3":
    print("Thank you. You have indicated that you plan to invest for ", timeframe, "months.")
    print(" ")
else:
    print("That is not a valid input. We will proceed with a default value of under 3 months.")
    print(" ")
    timeframe = "1"
    
# Figuring out how much $ the user wishes to invest. This will determine the recommendation of how many investments to select
amount = input("How much money do you plan to invest? $")

#Data validation for amount
try:
    float(amount)
    
    if float(amount) > 0:
        print("You have entered that you wish to invest $", amount, ".")
        amount = float(amount)
    else:
        print("You have entered a negative or 0 value. Using a default value of $1,000 instead.")
        amount = 1000
except:
    print("Your entry is not valid. We will proceed with a default value of $1,000")
    amount = 1000


    

# Telling the user that data will be processed now.
print(" ") #extra space for aesthetics
print("We will now process your data and recommend a list of securities.")

# Determining proper filters based on the timeframe.
if timeframe == "1":
    some_filters = [filters["P/E"]["Low (<15)"], filters["Country"]["USA"], filters["Target Price"]["10% Above Price"], filters["50-Day Simple Moving Average"]["Price 20 below SMA50"]]
    
elif timeframe == "2":

    some_filters = [filters["P/E"]["Under 20"], filters["Country"]["USA"], filters["Target Price"]["10% Above Price"], filters["Analyst Recom."]["Buy or better"], filters["50-Day Simple Moving Average"]["Price 20 below SMA50"]]
elif timeframe == "3":

    some_filters = [filters["P/E"]["Under 20"], filters["Country"]["USA"], filters["Target Price"]["20% Above Price"], filters["Analyst Recom."]["Buy or better"], filters["Sales growthpast 5 years"]["Over 10%"], filters["Debt/Equity"]["Under 0.2"]]

else:
    print("Try again.")

stock_list = Screener(filters=some_filters, order="ticker")

# Creating a csv with the stock recommendations
print(" ")
print("Downloading csv file with the stock recommendations...")
print(" ")
stock_list.to_csv("test_stocks.csv")

# Stock_data is a list that will hold the recommendations.
print("Retrieving stock data...")
stock_data = stock_list.get_ticker_details()

#counter variable to determine how many options there are
counter = 0

# Printing out the tickers of the recommended equities.
print(" ")
print("We have processed the data and recommend the following securities:")
for i in stock_data:
    print(i["Ticker"])
    counter = counter + 1

# User may either proceed or quit the program
print(" ")
proceed = input("Please type 'Yes' if you wish to proceed. Type anything else if you would like to quit. ")

# User chose to proceed
if proceed == "Yes" or proceed == "yes":
    print("We will now run through each of the recommended stocks, and you may indicate if you would like to include it in your portfolio or not.")
    
    #Giving the user a recommendation for how many equities to invest in, if the amount is less than 1000.
    if (amount < 1000):
        print(" ")
        print("Based on the amount of money that you are willing to invest, we would recommend selecting 5 of the ", counter, "recommended stocks.")

    #re-setting counter to 0
    counter = 1

    #new list to hold only the equities that the user picked
    portfolio = []

    #proceed with the program
    for i in stock_data:
        # Print detailed info on each equity
        print("Recommendation #", counter, ":")
        print("   Company: ", i["Company"], " Ticker:", i["Ticker"])
        print("   Description: ", i["Company"], " is in the ", i["Sector"], "and the ", i["Industry"], " industry.")
        print("                ", i["Company"], " has a market capitaliation of ", i["Market Cap"], "and a Price/Earnings ratio of ", i["P/E"], ".")
        print(" ")
        include = input("   Would you like to include this company in your portfolio? (Y/N)")

        # User input determines whether this company is included in the portfolio
        if include == "Y" or include == "y" or include == "yes":
            #include it
            portfolio.append(i["Ticker"])
            print("You have successfully included ", i["Ticker"], "in your portfolio.")
        elif include == "N" or include == "n" or include == "no":
            #do not include it
            print("We have excluded this company from your portfolio.")
        else:
            print("Your input was invalid so we have excluded this company from your portfolio.")
        
        #Print extra space
        print(" ")

        # Increasing counter by 1
        counter = counter + 1

    print("We have run through all of our recommendations.")

# Depending on how many equities the user chose, process the results
    if len(portfolio) == 0:
        # If user chose 0 equities, the program is over
        print("Unfortunately, you have chosen 0 of our recommendations. Goodbye.")
    elif len(portfolio) == 1:
        # If user chose just 1 equity, the program is over because that equity would receive 100% of the weight
        print("You have chosen 1 of our recommendations. Thank you for using our program and best of luck.")
    else:
        # If user chose multiple equities, the program can now run an additional step to recommend the best way to weight each equity.
        print("You have chosen to include the following securities in your portfolio:")
        print(portfolio)

        # Giving the user the option to add any other securities to their portfolio
        print("Would you like to add any securities to your portfolio?")
        add = input("Type yes to add securities, or no to keep the portfolio as is.")
        if add == "yes" or add == "Yes" or add == "Y" or add == "y":
            while add != "no" or add != "No":
                new = input("Please type the ticker of the security that you would like to add to your portfolio:")
                portfolio.append(new)
                add = input("Would you like to add another security to your portfolio? Type 'yes' or 'no'.")
                if add == "no" or "No":
                    break

        #Asks the user if they would like to quit or proceed
        print(" ")
        print("Would you like to proceed to the next step, where we will recommend what % weight to put in each equity?")
        proceed_to_suggested_weights = input("Type yes to proceed, or type anything else to quit.")
        if proceed_to_suggested_weights == "yes" or proceed_to_suggested_weights == "Yes" or proceed_to_suggested_weights == "y":

            # Run through recommended weights
            import yfinance as yf
            import numpy as np
            import scipy.optimize as sco

            noa = len(portfolio)
            raw = yf.download(portfolio, start="2015-01-01", end="2018-12-31")
            price_data=raw['Adj Close']
            rets = np.log(price_data / price_data.shift(1))
            
            mu=rets.mean() * 252
            VarCov=rets.cov() * 252
            rf=0.01

            initial_guess = [1./noa for x in range(noa)]
            cons = ({'type': 'eq', 'fun': lambda weights:  np.sum(weights) - 1})
            bnds = tuple((0, 1) for x in range(noa))
            opt_mve = sco.minimize(negative_sharpe, initial_guess, bounds=bnds, constraints=cons)
            mve_weights=opt_mve['x']
            print("The optimal weights are:", mve_weights)
            mve_ret = np.dot(mve_weights, mu)
            print("Based on past returns, you may expect a return of ", mve_ret)
            mve_vol = np.sqrt(np.dot(mve_weights,np.dot(VarCov, mve_weights.T)))
            print("Volatility:", mve_vol)
            


        else:
            print("Thank you for using the program. Goodbye.")






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