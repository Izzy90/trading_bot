import sys
import backtrader as bt


class TradeList(bt.Analyzer):

    def get_analysis(self):

        return self.trades

    def __init__(self):

        self.trades = []
        self.cumprofit = 0.0

    def notify_trade(self, trade):

        if trade.isclosed:

            broker_value = self.strategy.broker.getvalue()

            direction = 'long' if trade.history[0].event.size > 0 else 'short'

            price_in = trade.history[len(trade.history) - 1].status.price
            price_out = trade.history[len(trade.history) - 1].event.price
            date_in = bt.num2date(trade.history[0].status.dt)
            date_out = bt.num2date(trade.history[len(trade.history) - 1].status.dt)
            if trade.data._timeframe >= bt.TimeFrame.Days:
                date_in = date_in.date()
                date_out = date_out.date()

            percent_change = 100 * price_out / price_in - 100
            pnl = trade.history[len(trade.history) - 1].status.pnlcomm
            pnl_percent = 100 * pnl / broker_value
            bar_length = trade.history[len(trade.history) - 1].status.barlen
            p_bar = pnl / bar_length
            self.cumprofit += pnl

            size = value = 0.0
            for record in trade.history:
                if abs(size) < abs(record.status.size):
                    size = record.status.size
                    value = record.status.value

            highest_in_trade = max(trade.data.high.get(ago=0, size=bar_length + 1))
            lowest_in_trade = min(trade.data.low.get(ago=0, size=bar_length + 1))
            hp = 100 * (highest_in_trade - price_in) / price_in
            lp = 100 * (lowest_in_trade - price_in) / price_in
            if direction == 'short':
                mfe = -lp
                mae = -hp
            else:
                mfe = hp
                mae = lp

            self.trades.append({'ref': trade.ref, 'ticker': trade.data._name, 'dir': direction,
                                'datein': date_in, 'pricein': price_in, 'dateout': date_out, 'priceout': price_out,
                                'chng%': round(percent_change, 2), 'pnl': pnl, 'pnl%': round(pnl_percent, 2),
                                'size': size, 'value': value, 'cumpnl': self.cumprofit,
                                'nbars': bar_length, 'pnl/bar': round(p_bar, 2),
                                'mfe%': round(mfe, 2), 'mae%': round(mae, 2)})


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='')
    sys.stdout.flush()
    # Print New Line on Complete
    if iteration == total:
        print('\r%s |%s| %s%% %s' % (prefix, bar, 100, suffix), end='')


# def convert_value_to_coins(value, price):

def save_plots(cerebro, numfigs=1, iplot=True, start=None, end=None,
               use=None, file_path='', **kwargs):
    from backtrader import plot
    if cerebro.p.oldsync:
        plotter = plot.Plot_OldSync(**kwargs)
    else:
        plotter = plot.Plot(**kwargs)

    figs = []
    for stratlist in cerebro.runstrats:
        for si, strat in enumerate(stratlist):
            rfig = plotter.plot(strat, figid=si * 100,
                                numfigs=numfigs, iplot=iplot,
                                start=start, end=end, use=use)
            figs.append(rfig)

    for fig in figs:
        for f in fig:
            f.savefig(file_path, bbox_inches='tight')
    return figs


if __name__ == "__main__":
    pass
