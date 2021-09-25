import strategies

# IO options
show_progress_bar = True

# Params: symbols, intervals, test periods & strategies to backtest
symbols = [
    'BNBBUSD',
    'BTCBUSD'
]
intervals = [
    '1h',
    # '1m'
]
periods = [
    # ['1 March 2021', '4 March 2021'],
    ['3 March 2021', '17 March 2021'],
    ['1 January 2021', '1 September 2021'],
    ['1 February 2020', '1 October 2020'],
    ['1 March 2020', '1 November 2020'],
    ['1 April 2020', '1 December 2020'],
]
strategies_list = [
                    strategies.SmaCross,
                    strategies.RSIStrategy,
                    strategies.BuyAndHold
                    # strategies.SMACheating,
                   ]
additional_params = {
    'SmaCross':
        {
            'slow_mas': [i for i in range(30, 360, 30)],
            'fast_mas': [
                1,
                10,
            ],
        },
    'RSIStrategy': {},
    'BuyNHold': {},
}

# Configurations
trade_commission_percentage = 0.001  # this isn't formatted as a % (commissions = 1 corresponds to 100% commission)
data_folder_name = 'data'
plots_folder_name = 'plots'
output_folder_name = 'out'


if __name__ == "__main__":
    pass
