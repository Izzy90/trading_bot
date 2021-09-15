import strategies


symbols = ['BNBBUSD', 'BTCBUSD']

# Params: intervals, test periods
intervals = [
    '1h',
    # '1m'
]
periods = [
    # ['1 March 2021', '4 March 2021'],
    ['3 March 2021', '17 March 2021'],
    ['1 January 2021', '1 September 2021'],

]
strategies_list = [
                    strategies.SmaCross,
                    # strategies.RSIStrategy   # this one is buggy
                   ]
trade_commission_percentage = 0.1


data_folder_name = 'data'
plots_folder_name = 'plots'
output_folder_name = 'out'

show_progress_bar = True
show_plots = False


if __name__ == "__main__":
    pass
