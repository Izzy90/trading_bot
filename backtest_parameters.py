import strategies


symbols = ['BNBBUSD', 'BTCBUSD']
# Params: intervals, test periods
intervals = [
    '5m',
    '1m'
]
periods = [
    ['1 March 2021', '2 March 2021'],
    ['3 March 2021', '13 March 2021'],
    ['1 July 2021', '1 August 2021']
]
strategies_list = [
                    strategies.SmaCross,
                   # strategies.RSIStrategy   # this one is buggy
                   ]
trade_commission_percentage = 0.1
data_folder_name = 'data'
plots_folder_name = 'plots'


if __name__ == "__main__":
    pass
