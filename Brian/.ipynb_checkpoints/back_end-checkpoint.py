
#imports that we need
import requests
import json
import csv
import pandas as pd
import os.path
import numpy as np
import matplotlib.pyplot as plt


#API_KEY FOR ALPHAVANTAGE API !DO NOT TOUCH!
API_KEY = '4HNDQOUQ2A1G90RW'

#api link for later if we want to use [news and things like that]
#api_url = https://api.iextrading.com/1.0/stock/aapl/batch?types=quote,news,chart&range=1m&last=10

#api link for stock twits and sentiment analysis if we want
#https://api.stocktwits.com/api/2/streams/symbol/AAPL.json



'''
#this is a test function to see if we can streamline code. Dont touch/worry about this right now
def pass_symbol(symbol_passed):
    global symbol
    symbol = symbol_passed
    return
'''

#makes a list of inuts for the user to enter to  
def get_stocks():
    
    stock_symbols = []
    while True:
        symbol = input("Enter a stock symbol: ").upper()
        
        if len(stock_symbols) >= 4 or symbol.lower() == "no":
            break
        else:
            stock_symbols.append(symbol)
    return(stock_symbols)

#this function makes the dataframe from the CSV given from teh API. It cleans up the rows and sets the index column to the dates
def make_df(symbol):
    
    #Dont use this one for testing, only deployemnt
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + symbol + '&outputsize=full&datatype=csv&apikey=' + API_KEY

    #generates the URL based on the symbol imported and gets the JSON data from the API if file hasn't been written before
    #url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + symbol + '&outputsize=compact&datatype=csv&apikey=' + API_KEY
    data = pd.read_csv(url, index_col="timestamp", parse_dates = True, na_values = ' ')
    data['close'] = data['adjusted_close']
    data.index.names = ['date']
    print("DF Created!")
    return (data)


#adding oc_var, volatility, fluctuation, MA(5), MA(30) & MA(252)
def mod_df(df):
    df['fluctuation'] = 100*(df['high']-df['low'])/df['close']
    df['oc_var'] = df['open'] - df['close']
    df['volatility'] = df['high'] - df['low']
    df['ma(5)'] = df['close'].rolling(5).mean()
    df['ma(50)'] = df['close'].rolling(50).mean()
    df['ma(200)'] = df['close'].rolling(200).mean()
    df['date'] = df.index
    df['dow'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['year'] = df['date'].dt.year
    
    
    
    rmse_ma5 = (((df['ma(5)'] - df['close'])**2).mean())**.5
    rmse_ma50 = (((df['ma(50)'] - df['close'])**2).mean())**.5
    rmse_ma200 = (((df['ma(200)'] - df['close'])**2).mean())**.5
    print("RMSE of MA(5) is: ", '{:,.2f}'.format(rmse_ma5)) 
    print("RMSE of MA(50) is: ", '{:,.2f}'.format(rmse_ma50))
    print("RMSE of MA(200) is: ", '{:,.2f}'.format(rmse_ma200))
    return (df)


#makes a summary of todays stock information
def todays_summary(df):
    open_price = '${:,.2f}'.format(df.iloc[0]['open'])
    high_price = '${:,.2f}'.format(df.iloc[0]['high'])
    low_price = '${:,.2f}'.format(df.iloc[0]['low'])
    close_price = '${:,.2f}'.format(df.iloc[0]['close'])
    volume = "{:,}".format(int(df.iloc[0]['volume']))
    fluctuation = '{:.2f}'.format(df.iloc[0]['fluctuation'])
    
    print("Todays Opening Price: ", open_price)
    print("Todays Highest Price: ", high_price)
    print("Todays Lowest Price: ", low_price)
    print("Todays Closing Price: ", close_price)
    print("Todays Trading Volume: ", volume)
    print("Todays Price Fluctuation: ", str(fluctuation) + "%")
    return



def plot_price_vs_dow(df):
    
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    week_df = df['close'].groupby(df['dow']).mean().reindex(days)
    
    upper_limit = week_df.max()
    lower_limit = week_df.min()
    
    upper_limit = upper_limit + (upper_limit*0.01)
    lower_limit = lower_limit - (lower_limit*0.01)
    
    week_df.plot(color ='r', label ='AMZN', kind = 'bar', ylim=(lower_limit,upper_limit))
    plt.legend()
    plt.show()

    return

def plot_price_vs_month(df):
    
    months = ['January','February','March','April','May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_df = df['close'].groupby(df['month']).mean().reindex(months)
    
    upper_limit = month_df.max()
    lower_limit = month_df.min()
    
    upper_limit = upper_limit + (upper_limit*0.01)
    lower_limit = lower_limit - (lower_limit*0.01)
    
    month_df.plot(color ='r', label ='AMZN', kind = 'bar', ylim=(lower_limit,upper_limit))
    plt.legend()
    plt.show()

    return


#diaplsy the  close price vs date in a graph 
def plot_price_vs_time(df):
    df['close'].plot(color ='r', label ='AMZN')
    plt.legend()
    plt.show()
    return

#plot the flucuation by day 
def plot_fluc_vs_time(df):
    df['fluctuation'].plot(color ='r', label ='AMZN')
    plt.legend()
    plt.show()
    return


#plot the volume vs volatiltiy
def plot_volume_vs_volatiltiy(df):
    volume = df['volume']
    volatility = df['volatility']
    
    correlation = df['volume'].corr(df['fluctuation'])
    print('Correlation: ',correlation)
   #format and display plot
    plt.scatter(x = volatility, y = volume, c='b', alpha = .2)
    plt.xlabel('Volatility')
    plt.ylabel('Volume')
    plt.show();
    return


#gets todays news articles for the stock 
def news(symbol):
    
    url = 'https://api.iextrading.com/1.0/stock/' + symbol.lower() + '/batch?types=news&last=5'
    news = requests.get(url)
    news_json_str = news.content
    news_data = json.loads(news_json_str)
    
    print('\033[1m' + "Todays News", '\n')
    for x in range(0,5):
        news_headline = news_data['news'][x]['headline']
        output = str(x) + ") " + news_headline
        print('\033[0m' + output)
    return