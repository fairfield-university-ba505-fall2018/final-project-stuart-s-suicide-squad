#latest Test
#imports that we need
import requests
import json
import csv
import pandas as pd
import os.path

#API_KEY  !DO NOT TOUCH!
API_KEY = '4HNDQOUQ2A1G90RW'

def test_fun():
    #symbol = input("Enter a stock symbol: ").upper()
    print("test worked")
    return


#get the JSON values for the entred symbols
def alphaVantageJSON(symbol):

    # Use this API when calling the full data files
    #url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&outputsize=full&apikey=' + API_KEY
    
    #generates the URL based on the symbol imported and gets the JSON data from the API. 
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&outputsize=compact&apikey=' + API_KEY
    
    
    alphaVantage = requests.get(url)
    alphaVantage_json_str = alphaVantage.content
    alphaVantage_data = json.loads(alphaVantage_json_str)
    
   
    #gets all the 'days' as the keys from the JSON 
    days = alphaVantage_data['Time Series (Daily)'].keys()
    
    #get the open price for every day
    for k in days:
        date = str(k)
        open_price = alphaVantage_data['Time Series (Daily)'][date]['1. open']
        open_price_float = float(open_price)
        
        
        #works but converts them to a string for pretty output
        open_price_round = '${:,.2f}'.format(open_price_float)
        
        print(k + " Open Price: " + open_price_round)
    
    return



#get the CSV values for the entred symbols from the API
def alphaVantageCSV(symbol):

    csv_name = 'csv_files/' + symbol.lower() + "_data.csv"
    
    
    #write new CSV file
    if os.path.isfile(csv_name) != True:
    
        #Dont use this one for testing, only deployemnt
        #url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&outputsize=full&datatype=csv&apikey=' + API_KEY
        
        
        #generates the URL based on the symbol imported and gets the JSON data from the API if file hasn't been written before
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&outputsize=compact&datatype=csv&apikey=' + API_KEY
        
        
        data = pd.read_csv(url)
        csv_name = 'csv_files/' + symbol.lower() + "_data.csv"
        data.to_csv(csv_name)
        print("Writing New File... One Moment")
        
    #update current CSV file
    else:
        print("Updating current file... One Moment")
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&outputsize=compact&datatype=csv&apikey=' + API_KEY
        data = pd.read_csv(url)
        csv_name = 'csv_files/' + symbol.lower() + "_data.csv"
        data.to_csv(csv_name)
    
    return

