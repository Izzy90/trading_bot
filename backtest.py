import backtrader as bt
from typing import Type
import strategies


class BackTest:
    strategy = None
    data_file_path = ''

    def __init__(self, strategy: Type[bt.Strategy], data_file_path: str):
        self.strategy = strategy
        self.data_file_path = data_file_path

    def run_backtest(self):
        cerebro = bt.Cerebro()
        data = bt.feeds.GenericCSVData(dataname=self.data_file_path, dtformat=2)
        cerebro.adddata(data)
        cerebro.addstrategy(self.strategy)
        cerebro.addobserver(bt.observers.Broker)
        cerebro.addobserver(bt.observers.Trades)
        cerebro.addobserver(bt.observers.BuySell)
        cerebro.run(
            # Un-comment to disable default observers
            stdstats=False
        )
        cerebro.plot()
        # TODO - save backtest results (to some pandas df) and return it?


if __name__ == '__main__':
    data_file_path = 'BNBBUSD_5m.csv'
    strategy = strategies.SmaCross
    my_backtest = BackTest(strategy=strategy, data_file_path=data_file_path)
    my_backtest.run_backtest()
