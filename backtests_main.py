import pandas as pd
from get_data import get_historical_data
from binance.client import Client
import config
import strategies
from backtest import BackTest


def main():
    # todo: Generate a list of all Binance symbols (or just hardcode the symbols we're interested in testing)
    symbols = ['BNBBUSD', 'BTCBUSD']

    # Params: intervals, test periods
    intervals = ['5m']
    periods = [
        # ['1 March 2021', '2 March 2021'],
        ['1 March 2021', '1 April 2021'],
        ['1 July 2021', '1 August 2021']
    ]
    strategies_list = [strategies.SmaCross]

    # Init client
    client = Client(config.API_KEY, config.API_SECRET)

    # Init results df
    results_df = pd.DataFrame()

    # For each symbol, interval, period, strategy:
    for symbol in symbols:
        for interval in intervals:
            for period in periods:
                for strategy in strategies_list:
                    # Get_data - fetch historical data for the current params
                    data_filename = get_historical_data(client=client, symbol=symbol, interval=interval,
                                                        start_date=period[0], end_date=period[1])
                    # Backtest it
                    my_backtest = BackTest(strategy=strategy, data_file_path=data_filename)
                    # todo: add results to results df
                    my_backtest.run_backtest()

    # todo: analyze results df to show how the strategy performs

    return


if __name__ == '__main__':
    main()
