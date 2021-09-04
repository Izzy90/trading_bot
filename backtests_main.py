import pandas as pd
from get_data import get_historical_data
from binance.client import Client
import config
import strategies
from backtest import BackTest
import os
from backtest_parameters import *


def main():
    # todo: Generate a list of all Binance symbols (or just hardcode the symbols we're interested in testing)


    # Init client
    client = Client(config.API_KEY, config.API_SECRET)

    # Init results df
    results_df = pd.DataFrame()

    # create data folder
    if not os.path.exists(data_folder_name):
        os.makedirs(data_folder_name)

    # For each symbol, interval, period, strategy:
    for symbol in symbols:
        for interval in intervals:
            for period in periods:
                for strategy in strategies_list:

                    # Get_data - fetch historical data for the current params
                    data_filename = get_historical_data(client=client, symbol=symbol, interval=interval,
                                                        start_date=period[0], end_date=period[1],
                                                        folder=data_folder_name)
                    # Backtest it
                    my_backtest = BackTest(strategy=strategy, data_file_path=data_filename)
                    # todo: add results to results df
                    # TODO: fix bug here:
                    my_backtest.run_backtest(window_size=270)

    # todo: analyze results df to show how the strategy performs

    return


if __name__ == '__main__':
    main()
