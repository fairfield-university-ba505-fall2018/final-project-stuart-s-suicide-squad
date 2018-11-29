
#imports that we need
import requests
import json
import csv
import pandas as pd
import os.path
import numpy as np
import matplotlib.pyplot as plt


#API_KEY  !DO NOT TOUCH!
API_KEY = '4HNDQOUQ2A1G90RW'

def make_df(symbol):
    
    #Dont use this one for testing, only deployemnt
    #url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&outputsize=full&datatype=csv&apikey=' + API_KEY

    #generates the URL based on the symbol imported and gets the JSON data from the API if file hasn't been written before
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&outputsize=compact&datatype=csv&apikey=' + API_KEY
    data = pd.read_csv(url, index_col="timestamp", parse_dates = True)
    data.index.names = ['Date']
    

    return (data)


def show_data(df):
    df['close'].plot(color ='r', label = symbol_save)
    df['open'].plot(color ='b', label = symbol_save)
    plt.legend()
    plt.show()
    return


def test(symbol):
    global symbol_save
    symbol_save = symbol
    return

    