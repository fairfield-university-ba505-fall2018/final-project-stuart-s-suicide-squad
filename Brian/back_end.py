
#imports that we need
import requests
import json
import csv
import pandas as pd
import os.path
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from textblob import TextBlob

#API_KEY FOR ALPHAVANTAGE API !DO NOT TOUCH!
API_KEY = '4HNDQOUQ2A1G90RW'

#api link for stock twits and sentiment analysis if we want
#https://api.stocktwits.com/api/2/streams/symbol/AAPL.json



#makes a list of inputs for the user to enter to  
def get_stocks():
    stock_symbols = []
    symbol = ""
    
    while True:
        #symbol = input("Enter a stock symbol: ").upper()
        if len(stock_symbols) >= 4 or symbol.lower() == "no":
            break
        else:
            symbol = input("Enter a stock symbol: ").upper()
            if symbol.lower() != "no":
                stock_symbols.append(symbol)
    return(stock_symbols)


#makes DF's from the passed list of symbols, makes theindex column dates with a dateTime object, overwrites the 'close' column with an adjusted value to include splits in price
def make_df(symbols): 

    stock_df = []
    
    for x in symbols:
        #Dont use this one for testing, only deployemnt
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + x + '&outputsize=full&datatype=csv&apikey=' + API_KEY
        
        #use this one for testing
        #url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + x + '&outputsize=compact&datatype=csv&apikey=' + API_KEY
        data = pd.read_csv(url, index_col="timestamp", parse_dates = True, na_values = ' ')
        data['close'] = data['adjusted_close']
        data.index.names = ['date']
        stock_df.append(data)
    
    return(stock_df)

#adding oc_var, volatility, fluctuation, MA(5), MA(50) & MA(200)
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

    return (df)



def predict(df):
    rmse_ma5 = (((df['ma(5)'] - df['close'])**2).mean())**.5
    rmse_ma50 = (((df['ma(50)'] - df['close'])**2).mean())**.5
    rmse_ma200 = (((df['ma(200)'] - df['close'])**2).mean())**.5
    print("RMSE of MA(5) is: ", '{:,.2f}'.format(rmse_ma5)) 
    print("RMSE of MA(50) is: ", '{:,.2f}'.format(rmse_ma50))
    print("RMSE of MA(200) is: ", '{:,.2f}'.format(rmse_ma200))
    
    return

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
    print("Todays Price Fluctuation: ", str(fluctuation) + "%" + '\n')
    return



def plot_price_vs_dow(df, symbol):
    
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    week_df = df['close'].groupby(df['dow']).mean().reindex(days)
    
    upper_limit = week_df.max()
    lower_limit = week_df.min()
    
    upper_limit = upper_limit + (upper_limit*0.01)
    lower_limit = lower_limit - (lower_limit*0.01)
    
    week_df.plot(color ='r', label =symbol, kind = 'bar', ylim=(lower_limit,upper_limit))
    plt.legend()
    plt.show()

    return

def plot_price_vs_month(df, symbol):
    
    months = ['January','February','March','April','May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_df = df['close'].groupby(df['month']).mean().reindex(months)
    
    upper_limit = month_df.max()
    lower_limit = month_df.min()
    
    upper_limit = upper_limit + (upper_limit*0.01)
    lower_limit = lower_limit - (lower_limit*0.01)
    
    month_df.plot(color ='r', label = symbol, kind = 'bar', ylim=(lower_limit,upper_limit))
    plt.legend()
    plt.show()

    return


#diaplsy the  close price vs date in a graph 
def plot_price_vs_time(df, symbol):
    df['close'].plot(color ='r', label = symbol)
    plt.legend()
    plt.show()
    return

#plot the flucuation by day 
def plot_fluc_vs_time(df, symbol):
    df['fluctuation'].plot(color ='r', label = symbol)
    plt.legend()
    plt.show()
    return


#plot the volume vs volatiltiy
def plot_volume_vs_volatiltiy(df, symbol):
    volume = df['volume']
    volatility = df['volatility']
    
    correlation = volume.corr(volatility)
    print('Correlation1: ',correlation)
   #format and display plot
    plt.scatter(x = volatility, y = volume, c='b', alpha = .2)
    plt.xlabel('Volatility')
    plt.ylabel('Volume')
    plt.title(symbol)
    plt.show();
    return


#gets todays news articles for the stock 
def news(symbol):
    
    sleep(3)
    url = 'https://api.iextrading.com/1.0/stock/' + symbol.lower() + '/batch?types=news&last=5'
    news = requests.get(url)
    news_json_str = news.content
    news_data = json.loads(news_json_str)
    length = len(news_data['news'])
    
    for x in range(0,length):
        
        news_headline = news_data['news'][x]['headline']
        sentiment = sent_analysis(news_headline)
        output = str(x + 1) + ") " + news_headline + "[" + sentiment + "]"
        print('\033[0m' + output)
        
    print('\n')
    
    return


def sent_analysis(headline):
    testimonial = TextBlob(headline)
    sentiment = float(testimonial.sentiment.polarity) * 100
    sent_formatted = '{:.1f}'.format(sentiment)
    string_sent = str(sent_formatted) + "%"
    
    return(string_sent)
