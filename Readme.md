## Project Background

Brought to you by: Brian Walsh, Thomas Moroski and Stuart Weinstein

Our goal was to develop an interactive dashboard where users can get descriptive statistics on any US stock.

## How to Run our Program

Everything you need to run the program is already pre-installed. The only package that you are missing is textblob that is used for sentiment analysis. In order to download this package you will need to use the pip command in terminal as follows 
`pip install --user textblob`
This will allow you to simply run the program through the jupyter notebook. 

## Sections 

1. The end user may add up to 4 stock ticker symbols
2. The application will then provide a quick analysis including Fluctuation, Volatility, % Term Moving Average, 5, 50 and 200 day Moving Averages.
3. A one step ahead forecast of the next price is provided with the RMSE (Root Mean Square Error score provided)for each Moving Average
4. A current summary of the day's performance for each ticker is provided
5. A series of charts: price vs. time, fluctuation vs. time and volume vs. time are provided
6. Finally, news articles are provided as well as the last 30 'tweets' from stock twits. At the end of each line, there is a % value in [] which indicates the sentiment value of the headline/tweet. It is on a continous scale from [-1 : 1] and the value is shown as a % value. 0 is a neutral headline.

## Resources
If there are any issues please reach out to brian.walsh@student.fairfield.edu or stuart.weinstein@student.fairfield.edu or thomas.moroski@student.fairfield.edu