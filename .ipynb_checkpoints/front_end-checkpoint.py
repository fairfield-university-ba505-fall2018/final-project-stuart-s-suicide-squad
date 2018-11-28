#Initial Imports

import back_end as bk


symbol = input("Enter a stock symbol: ").upper()
#bk.alphaVantageJSON(symbol)
bk.alphaVantageCSV(symbol)