import backtrader as bt
from typing import Type
import os
from backtest_parameters import *
from utils.misc import TradeList, save_plots
import matplotlib.pyplot as plt
import pandas as pd


class BackTest:

    strategy = None
    data_file_path = ''

    def __init__(self, strategy: Type[bt.Strategy], data_file_path: str, strategy_specific_params=None):
        self.strategy = strategy
        self.data_file_path = data_file_path
        self.strategy_specific_params = strategy_specific_params

    def run_backtest(self, **kwargs):
        cerebro = bt.Cerebro(cheat_on_open=True)
        data = bt.feeds.GenericCSVData(
            dataname=self.data_file_path,
            openinterest=-1,
            timeframe=bt.TimeFrame.Minutes,
            dtformat=2
        )

        cerebro.adddata(data)
        cerebro.addstrategy(self.strategy, **self.strategy_specific_params)
        cerebro.addobserver(bt.observers.Broker)
        cerebro.addobserver(bt.observers.Trades)
        cerebro.addobserver(bt.observers.BuySell)
        cerebro.addanalyzer(TradeList, _name='trade_list')
        cerebro.broker.setcommission(commission=trade_commission_percentage)
        strat = cerebro.run(
            # Un-comment to disable default observers
            stdstats=False,
            tradehistory=True
        )
        curr_plots_folder_name = f"{kwargs['curr_config_folder']}"
        if not os.path.exists(curr_plots_folder_name):
            os.makedirs(curr_plots_folder_name)

        # TODO: would we want more than just the trades list? Missed opportunities? Also, add cash to trades log
        # Save trade list
        trade_list = strat[0].analyzers.getbyname("trade_list").get_analysis()
        df = pd.DataFrame(trade_list)
        df.to_csv(f"{kwargs['curr_config_folder']}/trades.csv")

        # Save plot
        plt.rcParams["figure.figsize"] = (18, 8)
        save_plots(cerebro, file_path=f"{plots_folder_name}/{kwargs['curr_config_name']}.jpg")
        save_plots(cerebro, file_path=f"{curr_plots_folder_name}/{kwargs['curr_config_name']}.jpg")
        plt.close()


if __name__ == '__main__':
    pass
