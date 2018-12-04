
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
    #url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol_save + '&outputsize=full&datatype=csv&apikey=' + API_KEY

    #generates the URL based on the symbol imported and gets the JSON data from the API if file hasn't been written before
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&outputsize=compact&datatype=csv&apikey=' + API_KEY
    data = pd.read_csv(url, index_col="timestamp", parse_dates = True, na_values = ' ')
    data.index.names = ['date']
    print("DF Created!")
    return (data)


#makes new columns to add to the DF it is passed
def add_fluctuation(df):
    df['fluctuation'] = 100*(df['high']-df['low'])/df['close']
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
    print("Todays Price Fluctuation: ", fluctuation,"%")
    return


#diaplsy the open and close price vs date in a graph 
def graph(df,symbol):
    df['close'].plot(color ='r', label = symbol)
    df['open'].plot(color ='b', label = symbol)
    plt.legend()
    plt.show()
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
        news_url = news_data['news'][x]['url']
        output = str(x) + ") " + news_headline + " [URL:" + news_url + "]"
        print('\033[0m' + output)
    return