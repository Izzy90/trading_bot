import config
import csv
from binance.client import Client

data_path = 'data'


# This function will generate a csv dataset of a chosen symbol, in a chosen frequency, for a chosen time period.
# Dates format should be "1 July, 2021"
def get_historical_data(client: Client, symbol: str, interval: str, start_date: str, end_date: str,
                        folder: str):

    csv_filename = f'{folder}/{symbol}_{interval}_{start_date}-{end_date}.csv'
    csvfile = open(csv_filename, 'w', newline='')
    candlestick_writer = csv.writer(csvfile, delimiter=',')

    candlesticks = client.get_historical_klines(symbol, interval, start_date, end_date)

    for candlestick in candlesticks:
        candlestick[0] = int(candlestick[0] / 1000)
        candlestick_writer.writerow(candlestick)

    csvfile.close()
    return csv_filename


if __name__ == "__main__":
    client = Client(config.API_KEY, config.API_SECRET)
    a = get_historical_data(client=client, symbol='BNBBUSD', interval='5m', start_date='1 March 2021',
                            end_date='1 April 2021', folder='demo_data')
    print(a)
