import backtrader as bt
import talib
import numpy as np


# TODO 1: re-format all strategies to handle the buy/sell decisions as meeting a set of conditions.
#  This will help logging. Optional: frame the decision as a decision tree, to enable more scenarios more complex than
#  simple 'and' on all conditions.
# TODO 2 (optional): Create a my_strategy class, subclass of bt.Strategy and superclass of all other strategies here,
#   in order to mitigate code duplication and provide a single template for strategies
# TODO 3: Enable strategies to support jumping between pairs, rather than just looking at a single pair
# TODO 4: Enable strategies to support multiple time-periods for more complex calculations


class RSIStrategy(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        buy_ratio=0.7,  # to avoid trying to buy with more cash than we actually have
        verbose=False,
    )
    display_name = 'RSIStrategy'

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data)

    # size = amount of coin to buy (etc. BTC)
    def next(self):
        if self.rsi < 30 and not self.position:
            amount = self.broker.cash / self.datas[0].close[0] * self.p.buy_ratio
            self.buy(size=amount)  # enter long
        if self.rsi > 70 and self.position:
            self.close()


class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pcurr_price=1,  # period for the fast moving average
        pfast=1,  # period for the fast moving average
        # pslow=270,  # period for the slow moving average
        buy_ratio=0.7,  # to avoid trying to buy with more cash than we actually have
        verbose=False,
    )
    display_name = 'SmaCross'

    def __init__(self, **kwargs):
        self.curr_price = bt.ind.SMA(period=self.p.pcurr_price)  # fast moving average
        self.order = None,
        self.sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        self.sma2 = bt.ind.SMA(period=kwargs['window_sizes'])  # slow moving average
        self.crossover = bt.ind.CrossOver(self.sma1, self.sma2)  # crossover signal

    def next(self):

        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                amount = self.broker.cash / self.datas[0].close[0] * self.p.buy_ratio
                self.buy(size=amount)  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            # TODO: find a way to not sell cheaper than what I bought? (Including commissions) - set a limit
            self.close()  # close long position

    def notify_trade(self, trade):
        if trade.isclosed:
            self.log('TRADE PROFIT, GROSS %.2f, NET %.2f' %
                     (trade.pnl, trade.pnlcomm))
        elif trade.justopened:
            self.log('TRADE OPENED, SIZE %2d' % trade.size)

    def notify_order(self, order):
        if order.status in [bt.Order.Submitted, bt.Order.Accepted]:
            return  # Await further notifications

        if order.status == order.Completed:
            if order.isbuy():
                buytxt = 'BUY COMPLETE, %.2f' % order.executed.price
                self.log(buytxt, order.executed.dt)
            else:
                selltxt = 'SELL COMPLETE, %.2f' % order.executed.price
                self.log(selltxt, order.executed.dt)

        elif order.status in [order.Expired, order.Canceled, order.Margin]:
            self.log('%s ,' % order.Status[order.status])
            pass  # Simply log

        # Allow new orders
        self.order = None

    def log(self, txt, dt=None):
        if self.p.verbose:
            dt = dt or self.data.datetime[0]
            dt = bt.num2date(dt)
            print('%s, %s' % (dt.isoformat(), txt))


# # TODO - Exponential MA
# class EmaCross(bt.Strategy):

# TODO - Buy and Hold: Baseline Strategy
class BuyAndHold(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pcurr_price=1,  # period for the fast moving average
        pfast=1,  # period for the fast moving average
        # pslow=270,  # period for the slow moving average
        buy_ratio=0.7,  # to avoid trying to buy with more cash than we actually have
        verbose=False,
    )
    display_name = 'BuyNHold'

    def next(self):
        # just buy
        if not self.position:  # not in the market
            amount = self.broker.cash / self.datas[0].close[0] * self.p.buy_ratio
            self.buy(size=amount)  # enter long

# # TODO: Devise a strategy based on the asks and bids realtime data, or incorporate it in another strategy.
# class SupplyNDemand(bt.strategy):

# TODO: 1-2% per day strategy, 2x daily stop loss. Find a way to not stoploss too early in the day, something like a
#  stop-loss that decreases as the day progresses.
# class CompoundInterest(bt.strategy):
