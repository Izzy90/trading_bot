import backtrader as bt
from typing import Type
import strategies
import os
from backtest_parameters import *
from utils.misc import TradeList
import matplotlib.pyplot as plt
import pandas as pd


class BackTest:

    strategy = None
    data_file_path = ''

    def __init__(self, strategy: Type[bt.Strategy], data_file_path: str):
        self.strategy = strategy
        self.data_file_path = data_file_path

    def run_backtest(self, **kwargs):
        cerebro = bt.Cerebro()
        data = bt.feeds.GenericCSVData(
            dataname=self.data_file_path,
            openinterest=-1,
            timeframe=bt.TimeFrame.Minutes,
            dtformat=2
        )

        cerebro.adddata(data)
        if self.strategy == strategies.SmaCross:
            cerebro.addstrategy(self.strategy, kwargs['window_size'], kwargs['client'])
        else:
            cerebro.addstrategy(self.strategy)
        cerebro.addobserver(bt.observers.Broker)
        cerebro.addobserver(bt.observers.Trades)
        cerebro.addobserver(bt.observers.BuySell)
        cerebro.addanalyzer(TradeList, _name='trade_list')
        # cerebro.addwriter(bt.WriterFile, out='OUTPUT_FILE_PATH.txt')
        # cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio.txt')
        cerebro.broker.setcommission(commission=trade_commission_percentage)
        strat = cerebro.run(
            # Un-comment to disable default observers
            stdstats=False,
            tradehistory=True
        )
        curr_plots_folder_name = f"{kwargs['curr_config_folder']}"
        if not os.path.exists(curr_plots_folder_name):
            os.makedirs(curr_plots_folder_name)

        # Save trade list. TODO: would we want more than just the trades list?
        trade_list = strat[0].analyzers.getbyname("trade_list").get_analysis()
        df = pd.DataFrame(trade_list)
        # df = df.drop(['pnl/bar', 'ticker'], axis=1)
        df.to_csv(f"{kwargs['curr_config_folder']}/trades.csv")

        strat_name = f'{self.strategy}'.split('.')[1].split("'")[0]
        plt.rcParams["figure.figsize"] = (18, 8)
        if show_plots:
            cerebro.plot(savefig=True,
                         path=f"{curr_plots_folder_name}/{kwargs['curr_config_name']}.jpg",
                         # dpi=400,
                         # figs=30
                         )
        else:
            plt.savefig(fname=f"{curr_plots_folder_name}/{kwargs['curr_config_name']}.jpg")
        plt.savefig(fname=f"{plots_folder_name}/{kwargs['curr_config_name']}.jpg")
        plt.close()


if __name__ == '__main__':
    data_file_path = 'data/BNBBUSD_5m.csv'
    strategy = strategies.SmaCross
    my_backtest = BackTest(strategy=strategy, data_file_path=data_file_path)
    my_backtest.run_backtest()
