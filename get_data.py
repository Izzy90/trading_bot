import config
import csv 
import dateparser
from binance.client import Client
import binance

client = Client(config.API_KEY, config.API_SECRET)

#prices = client.get_all_tickers()

#for price in  prices:
#	print(price)

candles = client.get_klines(symbol='BNBBUSD', interval=Client.KLINE_INTERVAL_1MINUTE)

csvfile = open('BNB_MIN.csv', 'w', newline='')

txtfile = open('textfile.txt', 'w')

candlestick_writer = csv.writer(csvfile, delimiter=',')



#for candlestick in candles:
#	print(candlestick)

#	candlestick_writer.writerow(candlestick)

#print(len(candles))

#start =  binance.helpers.date_to_milliseconds(str(dateparser.parse('270 min ago UTC')))

#end =  binance.helpers.date_to_milliseconds(str(dateparser.parse('now')))

#print(start)
#print(end)


#candlesticks = client.get_historical_klines("BNBBUSD", Client.KLINE_INTERVAL_1MINUTE, start , end )


candlesticks = client.get_historical_klines("BNBBUSD", Client.KLINE_INTERVAL_1MINUTE, "1 July, 2021" , "31 July, 2021")


for candlestick in candlesticks:
	candlestick[0] = candlestick[0] / 1000
	candlestick_writer.writerow(candlestick)
	txtfile.write(str(candlestick))
	txtfile.write("\n")



csvfile.close()
txtfile.close()