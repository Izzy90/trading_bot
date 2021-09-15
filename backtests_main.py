import pandas as pd
from get_data import get_historical_data
from binance.client import Client
import config
from backtest import BackTest
import os
from backtest_parameters import *
from utils.misc import *
import datetime


def main():
    # Init client
    client = Client(config.API_KEY, config.API_SECRET)

    # Init results df
    results_df = pd.DataFrame()

    # create data folder
    if not os.path.exists(data_folder_name):
        os.makedirs(data_folder_name)
    # create output folder
    if not os.path.exists(output_folder_name):
        os.makedirs(output_folder_name)
    # create plots folder
    if not os.path.exists(plots_folder_name):
        os.makedirs(plots_folder_name)

    # Initialize progress bar
    num_of_configurations = len(symbols) * len(intervals) * len(periods) * len(strategies_list)
    print(f"Total number of configurations to backtest: {num_of_configurations}")
    configuration_number = 0

    # For each symbol, interval, period, strategy:
    for symbol in symbols:
        for interval in intervals:
            for period in periods:
                for strategy in strategies_list:

                    # Print progress bar
                    if show_progress_bar:
                        print_progress_bar(configuration_number, num_of_configurations)
                        configuration_number += 1

                    # Create the output folder for the current configuration
                    period_start_formatted = datetime.datetime.strptime(period[0], '%d %B %Y').strftime('%d%m%Y')
                    period_end_formatted = datetime.datetime.strptime(period[1], '%d %B %Y').strftime('%d%m%Y')
                    period_formatted = f"{period_start_formatted}-{period_end_formatted}"
                    # TODO: Add the window size for SMA as an optional suffix only for SMACross
                    curr_config_name = f"{interval}_{symbol}_{period_formatted}_{strategy.params.display_name}"
                    curr_config_folder = f"{output_folder_name}/{curr_config_name}"
                    if not os.path.exists(curr_config_folder):
                        os.makedirs(curr_config_folder)

                    # Get data - fetch historical data for the current params
                    data_filename = get_historical_data(client=client, symbol=symbol, interval=interval,
                                                        start_date=period[0], end_date=period[1],
                                                        folder=data_folder_name)
                    # Backtest it
                    my_backtest = BackTest(strategy=strategy, data_file_path=data_filename)
                    # todo: add results to results df

                    my_backtest.run_backtest(client=client, window_size=270, curr_config_folder=curr_config_folder,
                                             curr_config_name=curr_config_name)

    # optional todo: analyze results df to show how the strategy performs

    return


if __name__ == '__main__':
    main()
