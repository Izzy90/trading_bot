import backtrader as bt
from typing import Type
import strategies
import os
from backtest_parameters import *


class BackTest:
    strategy = None
    data_file_path = ''

    # TODO: add commissions

    def __init__(self, strategy: Type[bt.Strategy], data_file_path: str):
        self.strategy = strategy
        self.data_file_path = data_file_path

    def run_backtest(self, **kwargs):
        cerebro = bt.Cerebro()
        # TODO: Alter the timeframe parameter to be dynamic - when interval is in minutes, be minutes, etc.
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
        cerebro.addwriter(bt.WriterFile, out='OUTPUT_FILE_PATH.txt')
        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio.txt')
        cerebro.broker.setcommission(commission=trade_commission_percentage)
        cerebro.run(
            # Un-comment to disable default observers
            stdstats=False
        )
        if not os.path.exists(plots_folder_name):
            os.makedirs(plots_folder_name)
        # TODO - save backtest results (to some pandas df) and return it?
        strat_name = f'{self.strategy}'.split('.')[1].split("'")[0]
        cerebro.plot(savefig=True,
                     path=f'{plots_folder_name}/{kwargs["window_size"] if self.strategy == strategies.SmaCross else ""}_{strat_name}'
                     )


if __name__ == '__main__':
    data_file_path = 'data/BNBBUSD_5m.csv'
    strategy = strategies.SmaCross
    my_backtest = BackTest(strategy=strategy, data_file_path=data_file_path)
    my_backtest.run_backtest()
