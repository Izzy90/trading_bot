import backtrader as bt


# TODO 1: re-format all strategies to handle the buy/sell decisions as meeting a set of conditions.
#  This will help logging. Optional: frame the decision as a decision tree, to enable more scenarios more complex than
#  simple 'and' on all conditions.
# TODO 2 (optional): Create a my_strategy class (or AllInStrategy), subclass of bt.Strategy and superclass of all other
#  strategies here, in order to mitigate code duplication and provide a single template for strategies
# TODO 3: Enable strategies to support jumping between pairs, rather than just looking at a single pair
# TODO 4: Enable strategies to support multiple time-periods for more complex calculations


# TODO: Convert this strategy to use cheat on open
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


class SmaCross(bt.Strategy):        # This is the Cheat-on-Open version!
    params = dict(
        matype=bt.ind.SMA,          # Note: the MA type can also be a parameter, so no need for separate strategies!
    )
    display_name = 'SmaCross'

    def __init__(self, **kwargs):
        self.cheating = self.cerebro.p.cheat_on_open
        self.sma1 = self.p.matype(period=kwargs['fast_mas'])  # fast moving average
        self.sma2 = self.p.matype(period=kwargs['slow_mas'])  # slow moving average
        self.signal = bt.ind.CrossOver(self.sma1, self.sma2)  # crossover signal
        self.order = None

    def notify_order(self, order):
        if order.status != order.Completed:
            return
        self.order = None

    def operate(self):
        cheat_on_open_price = self.data.open[0]
        if self.order is not None:
            return
        if self.position:
            # TODO: find a way to not sell cheaper than what I bought? (Including commissions) - set a limit
            if self.signal < 0:
                self.order = self.close()
        elif self.signal > 0:
            size = self.broker.getcash() / cheat_on_open_price
            self.order = self.buy(
                size=size * 0.99
            )

    def next(self):
        if self.cheating:
            return
        self.operate()

    def next_open(self):
        if not self.cheating:
            return
        self.operate()


# # TODO - Exponential MA - can instead, incorporate an 'MA type' parameter into the SmaCross strategy
# class EmaCross(bt.Strategy):

# TODO - Convert this strategy to use cheat on open
class BuyAndHold(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        verbose=False,
        buy_ratio=0.7,  # to avoid trying to buy with more cash than we actually have
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
