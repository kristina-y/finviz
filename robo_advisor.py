#Here is my program. All of the code on this page is my own, except where noted that I adapted it from another source.

# Defining my functions:

# This will be necessary later on when suggesting weights
def negative_sharpe(weights, mu):
    weights = np.array(weights)
    pret = np.dot(weights, mu)
    pvol = np.sqrt(np.dot(weights,np.dot(VarCov, weights.T)))
    return -(pret-rf)/pvol

# Since my program collects a lot of user inputs, this function checks whether the user has said 'yes' or 'no'
def is_yes(user_input):
    if user_input == "yes" or user_input == "Yes" or user_input == "Y" or user_input == "y":
        return True
    else:
        return False

# Validating the $ amount entered by user
def validate_amount(how_much_to_invest):
    try:
        float(how_much_to_invest)
    
        if float(amount) > 0:
            print("You have entered that you wish to invest $", amount)
            return(float(amount))
        else:
            print("You have entered a negative or 0 value. Using a default value of $1,000 instead.")
            return(1000)
    except:
        print("Your entry is not valid. We will proceed with a default value of $1,000")
        return(1000)

# Validating and confirming the timeframe selected by the user
def validate_timeframe(user_choice):
    if user_choice == "1":
        print("Thank you. You have indicated that you plan to invest for 1-3 months.\n")
        return userchoice
    elif user_choice == "2":
        print("Thank you. You have indicated that you plan to invest for 3-6 months.\n")
        return user_choice
    elif user_choice == "3":
        print("Thank you. You have indicated that you plan to invest for 12+ months.\n")
        return user_choice
    else:
        print("That is not a valid input. We will proceed with a default value of under 3 months.\n")
        return "1"

# This function gives the user a recommendation of how many equities to invest in, based on the amount
def number_of_stocks(amount_to_invest):
    if (amount_to_invest < 500):
        print("\nBased on the amount of money that you are willing to invest, we would recommend selecting no more than 5 securities to invest in.")
    elif (amount_to_invest < 1000):
        print("\nBased on the amount of money that you are willing to invest, we would recommend selecting no more than 10 securities to invest in.")
    else:
        print("\nWe encourage you to diversify your portfolio as much as you can by selecting securities outside of our recommended list.")

# This function takes in a list of recommended stocks and runs through each option, giving the user a choice to include it or not.
def narrow_down_recommendations(list_of_options):
    counter = 1
    result = []
    for i in list_of_options:
        # Print detailed info on each equity
        print("Recommendation #", counter, "of", len(list_of_options), ":")
        print("   Company: ", i["Company"], " Ticker:", i["Ticker"])
        print("   Description: ", i["Company"], " is in the ", i["Sector"], "and the ", i["Industry"], " industry.")
        print("                ", i["Company"], " has a market cap of ", i["Market Cap"], "and a Price/Earnings ratio of ", i["P/E"], ".\n")
        include = input("   Would you like to include this company in your portfolio? (Y/N)  ")

        # User input determines whether this company is included in the portfolio
        if is_yes(include) == True:
            #include it
            result.append(i["Ticker"])
            print("You have successfully included ", i["Ticker"], "in your portfolio.\n")
        elif include == "N" or include == "n" or include == "no":
            #do not include it
            print("We have excluded this company from your portfolio.\n")
        else:
            print("Your input was invalid so we have excluded this company from your portfolio.\n")
            

        # Increasing counter by 1
        counter = counter + 1
    return result

from finviz.screener import Screener

# Get dictionary of available filters
filters = Screener.load_filter_dict()

# Welcome message:
print("Welcome to the short term robo advisor! Today, we will help you make an investment plan.")

print("First, what is your investment timeframe? Your three choices are as follows:")
print("    1. I plan to hold my investments for under 3 months")
print("    2. I plan to hold my investments for 3-12 months.")
print("    3. I plan to hold my investments for over 1 year.")

# This is for testing functions, so that inputs are only collected if the program is run through terminal
if __name__ == "__main__":
    # Determining investment timeframe (which will cause the algorithm to vary)
    timeframe = input("Please enter 1, 2, or 3 depending on how many months you intend to hold: ")

    # Data validation for timeframe
    timeframe = validate_timeframe(timeframe)
    
    # Figuring out how much $ the user wishes to invest. This will determine the recommendation of how many investments to select
    amount = input("How much money do you plan to invest? $")

    #Data validation for amount
    amount = validate_amount(amount)

    # Telling the user that data will be processed now.
    print("\nWe will now process your data and recommend a list of securities.")

    # Determining proper filters based on the timeframe.
    if timeframe == "1":
        some_filters = [filters["P/E"]["Low (<15)"], filters["Country"]["USA"], filters["Target Price"]["10% Above Price"], filters["50-Day Simple Moving Average"]["Price 20 below SMA50"], filters["IPO Date"]["More than a year ago"]]
    
    elif timeframe == "2":

        some_filters = [filters["P/E"]["Under 20"], filters["Country"]["USA"], filters["Target Price"]["10% Above Price"], filters["Analyst Recom."]["Buy or better"], filters["50-Day Simple Moving Average"]["Price 20 below SMA50"], filters["IPO Date"]["More than a year ago"]]
    elif timeframe == "3":

        some_filters = [filters["P/E"]["Under 20"], filters["Country"]["USA"], filters["Target Price"]["20% Above Price"], filters["Analyst Recom."]["Buy or better"], filters["Sales growthpast 5 years"]["Over 10%"], filters["Debt/Equity"]["Under 0.2"], filters["IPO Date"]["More than 5 years ago"]]

    else:
        print("Try again.")

    # Using API's Screener function to get the list of stocks
    stock_list = Screener(filters=some_filters, order="ticker")

    # Creating a csv with the stock recommendations
    print("\nDownloading csv file with the stock recommendations...\n")
    stock_list.to_csv("recommended_stocks.csv")

    # Stock_data is a list that will hold the recommendations.
    print("Retrieving stock data...")
    stock_data = stock_list.get_ticker_details()

    # Printing out the tickers of the recommended equities.
    print("\nWe have processed the data and recommend the following securities:")
    for i in stock_data:
        print(i["Ticker"])

    number_of_stocks(amount)
    
    print("\nWe will now run through each of the recommended stocks, and you may indicate if you would like to include it in your portfolio or not.")

    #new list to hold only the equities that the user picked
    portfolio = narrow_down_recommendations(stock_data)

    #proceed with the program
    print("We have run through all of our recommendations.\n")

    # Depending on how many equities the user chose, process the results
    if len(portfolio) == 0:
        # If user chose 0 equities, the program lets them quit or add their own securities
        print("Unfortunately, you have chosen 0 of our recommendations. Would you like to fill your portfolio with your own ideas?")
        next_step = input("Type 'yes' if you would like to add your own securities or 'quit' if you would like to exit the program. ")

    elif len(portfolio) == 1:
        # If user chose just 1 equity, the program lets them quit or add their own securities
        print("You have chosen 1 of our recommendations. Would you like to fill your portfolio with your own ideas?")
        next_step = input("Type 'yes' if you would like to add your own securities or 'quit' if you would like to exit the program. ")

    else:
        #automatically go onto the next step
        next_step = "yes"

    if is_yes(next_step) == True:
        # If user chose multiple equities, the program can now run an additional step to recommend the best way to weight each equity.
        print("\nYou have chosen to include the following securities in your portfolio:")
        print(portfolio)


        # Giving the user the option to add any other securities to their portfolio
        print("\nWould you like to add any securities to your portfolio?")
        add = input("Type yes to add securities, or no to keep the portfolio as is. ")
        while is_yes(add) == True:
            new = input("Please type the ticker of the security that you would like to add to your portfolio: ")
            portfolio.append(new)
            print("... Successfully added", new, "to the portfolio.\n")
            add = input("Would you like to add another security to your portfolio? Type 'yes' or 'no'. ")
                    

        #Asks the user if they would like to quit or proceed
        print("\nWould you like to proceed to the next step, where we will recommend what % weight to put in each equity?")
        proceed_to_suggested_weights = input("Type yes to proceed, or type anything else to quit. ")
        if is_yes(proceed_to_suggested_weights) == True:

            # Run through recommended weights
            # Some of the code in this section is adapted from my Principles of Investment Class (FINC 241)
                
            import yfinance as yf # Using yahoo finance historical returns
            import numpy as np
            import scipy.optimize as sco

            noa = len(portfolio)

            if timeframe == "1":
                # for the shortest timeframe, we are using the first 3 months of 2021
                raw = yf.download(portfolio, start="2021-01-01", end="2021-03-01")
                    
            elif timeframe == "2":
                # for the second to shortest timeframe, we are using the most recent 6 months
                raw = yf.download(portfolio, start="2020-12-01", end="2021-05-01")
                    
            else:
                # for the longest timeframe, we are using data from before covid
                raw = yf.download(portfolio, start="2019-01-01", end="2020-01-01")
                    
                
            price_data=raw['Adj Close']
            price_data.sort_index()
            rets = np.log(price_data / price_data.shift(1))
                
            mu=rets.mean() * 252
            VarCov=rets.cov() * 252
            rf=0.01

            # Constructing MVE portfolio
            initial_guess = [1./noa for x in range(noa)]
            cons = ({'type': 'eq', 'fun': lambda weights:  np.sum(weights) - 1})
            bnds = tuple((0, 1) for x in range(noa))
            opt_mve = sco.minimize(negative_sharpe, initial_guess, mu, bounds=bnds, constraints=cons)
            mve_weights=opt_mve['x']

                

            # Need to print output with weights
            portfolio.sort()

            i = 0
            print("The optimal weights are:")
            print("Ticker     Weight")
            while i < noa:
                    
                if len(portfolio[i]) == 3:
                    #printing an extra space if ticker is 3 characters
                    print(portfolio[i], "      ", "{:.2%}".format(mve_weights[i]))
                else:
                    print(portfolio[i], "     ", "{:.2%}".format(mve_weights[i]))

                i = i + 1
                
            # Will also give return and volatility
            mve_ret = np.dot(mve_weights, mu)
                
            mve_vol = np.sqrt(np.dot(mve_weights,np.dot(VarCov, mve_weights.T)))
                
            print("\nBased on past returns, you may expect a return of anywhere up to ", "{:.2%}".format(mve_ret), "and a volatility of ", "{:.2%}".format(mve_vol), "\n")

            print("If you choose to use our recommended weights, then you should invest the following $ in each security:")
            i = 0
                
            while i < noa:
                    
                if len(portfolio[i]) == 3:
                    print(portfolio[i], " : ", "${:,.2f}".format(mve_weights[i] * amount))
                else:   
                    print(portfolio[i], ": ", "${:,.2f}".format(mve_weights[i] * amount))

                i = i + 1


            print("\nThank you for using the short term robo advisor. Best of luck!")
                


        else:
            print("\nThank you for using the program. Goodbye.")

    else:
        print("\nThank you for using the program. Goodbye.")
