import backtrader as bt
import talib


# TODO: re-format all strategies to handle the buy/sell decisions as meeting a set of conditions. This will help logging


class RSIStrategy(bt.Strategy):

    def __init__(self):
        self.rsi = talib.RSI(self.data, timeperiod=14)

    # size = amount of coin to buy (etc. BTC)
    def next(self):
        if self.rsi < 30 and not self.position:
            self.buy(size=54)
        if self.rsi > 70 and self.position:
            self.close()


class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    # TODO: enable dynamic value for pslow MA window size as a parameter
    params = dict(
        pfast=1,  # period for the fast moving average
        pslow=270  # period for the slow moving average
    )

    def __init__(self, window_size, client):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=window_size)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):

        print(self.datetime.datetime())

        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                # TODO: The size is the number of coins to buy. Need to find a way to change this value with the total
                # amount of coin in the account
                amount = 2

                self.buy(size=amount)  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position


# TODO - Exponential MA
class EmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        # pfast=1,  # period for the fast moving average
        # pslow=270  # period for the slow moving average
    )

    def __init__(self):
        # sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        # sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        # self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal
        return

    def next(self):
        # if not self.position:  # not in the market
        #     if self.crossover > 0:  # if fast crosses slow to the upside
        #         self.buy(size=5.4)  # enter long
        #
        # elif self.crossover < 0:  # in the market & cross to the downside
        #     self.close()  # close long position
        return


# # TODO: Devise a strategy based on the asks and bids realtime data, or incorporate it in another strategy.
# class SupplyNDemand(bt.strategy):
#     # list of parameters which are configurable for the strategy
#     params = dict(
#     )
#
#     def __init__(self):
#         return
#
#     def next(self):
#         return


# # TODO: 1-2% per day strategy, 2x daily stop loss. Find a way to not stoploss too early in the day, something like a
# # stop-loss that decreases as the day progresses.
# class CompoundInterest(bt.strategy):
#     # list of parameters which are configurable for the strategy
#     params = dict(
#     )
#
#     def __init__(self):
#         return
#
#     def next(self):
#         return
