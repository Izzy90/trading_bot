import backtrader as bt
import talib


class RSIStrategy(bt.Strategy):

    def __init__(self):
        self.rsi = talib.RSI(self.data, timeperiod=14)

    # size = amount of coin to buy (etc. BTC)
    def next(self):
        if self.rsi < 30 and not self.position:
            self.buy(size=0.0000001)
        if self.rsi > 70 and self.position:
            self.close()


class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=1,  # period for the fast moving average
        pslow=270  # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy(size=5.4)  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position
