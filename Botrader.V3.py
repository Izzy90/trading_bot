import websocket, json, numpy, talib, config, pprint, dateparser, binance
from binance.enums import *
from binance.client import Client
import datetime
import os

#####  GLOBAL

MA = 21
TRADE_QUANTITY = 0.12
TRADE_SYMBOL = "BNBBUSD"
SOCKET = "wss://stream.binance.com:9443/ws/bnbbusd@kline_1m"
ORDER_TYPE_MARKET = 'MARKET'
BUFFER = 0.0005
BUDGET = 0
WIN = []

LOG_FILE_NAME = "logfile-200-5.txt"

if os.name == 'nt':
    import winsound

    WIN.append(True)
else:
    WIN.append(False)

###   KEYS

client = Client(config.API_KEY, config.API_SECRET)

#       Init budget
budget = []
budget.append(BUDGET)

#       Init buffers
buffer_up = 1 + BUFFER
buffer_down = 1 - BUFFER

print("Buffer up = %f" % buffer_up)
print("Buffer down  = %f" % buffer_down)
print("Budget: %f" % BUDGET)

#       Init past <MA> minutes prices back 
prices = []

go_back = '%d min ago UTC' % (MA)
start = str(dateparser.parse(go_back))
end = str(dateparser.parse('now'))

candlesticks = client.get_historical_klines(TRADE_SYMBOL, Client.KLINE_INTERVAL_1MINUTE, start, end)

for candlestick in candlesticks:
    prices.append(float(candlestick[4]))
print(prices)

#      Log file
logfile = open(LOG_FILE_NAME, 'w')
_ma = str(MA)
_buffer = str(BUFFER)
logfile.write("  There we Go!!    COIN:   %s  MA=   %s     BUFFER=    %s" % (TRADE_SYMBOL, _ma, _buffer))
logfile.write("\n")
logfile.close()

#       Init transactions

transactions = []


# TODO - What did Dean mean to do here?
def addTransaction(time, side, symbol, ex_amount, avarage_price):
    trans = trans.append(time, side, symbol, ex_amount, avarage_price)
    transactions.append(trans)
    # logfile.writerow(trans)
    return transactions


#       Orders function
def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        order = client.create_order(side=side, quantity=quantity, symbol=symbol, type=order_type)
        print("sending order")
        print(order)
        try:
            time = time.strftime("%Y-%m-%d %H:%M:%S")
            print("time: %s  BUY/Sell: %s   Coin: %s, Amount: %d, Price:  %s" % time, order.side, order.symbol,
                  order.quoteOrderQty, order.price)
            # addTransaction(time, order.side, order.symbol, order.quoteOrderQty, order.price)

        except Exception as e:
            print(e.message, "append Transaction error")

    except Exception as e:
        print(e.message, "error")
        return False

    return True


def on_open(ws):
    print('opened connection')


def on_close(ws):
    print('closed connection')


def on_message(ws, message):
    time = datetime.datetime.now()
    # print (time.strftime("%Y-%m-%d %H:%M:%S"))
    #   print(message)
    #   pprint.pprint(json_message)

    json_message = json.loads(message)

    # print("  There we Go!!    COIN:   %s  MA=   %s     BUFFER=    %s" % (TRADE_SYMBOL, _ma, _buffer  ))

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        prices.append(float(close))
        np_prices = numpy.array(prices)
        ma = talib.MA(np_prices, MA)
        ma = talib.MA(np_prices, MA)

        last_price = prices[-1]
        # check if can last_2_price is relevant
        last_2_price = prices[-2]
        last_ma = ma[-1]
        # check if can last_2_ma is relevant
        last_2_ma = ma[-2]
        last_budget = budget[-1]

        current_sell_limit = last_ma * buffer_down
        current_buy_limit = last_ma * buffer_up

        almost_order_zone = abs(last_price - (last_ma * BUFFER))
        if WIN[-1]:
            winsound.Beep(400, 100)

        print(time.strftime("%Y-%m-%d %H:%M:%S"))
        print("last_2_price: %f,  last_2_ma %f,  last_price %f,  last_ma %f, last_budget %d" % (
        last_2_price, last_2_ma, last_price, last_ma, last_budget))
        print(budget)
        print("Current_buy_limit     %f " % (current_buy_limit))
        print("Current_sell_limit:     %f " % (current_sell_limit))

        print("last_price     %f " % last_price)
        print("WIN= %r" % WIN[-1])
        if (last_budget == 1):
            if last_price > current_buy_limit:
                # 1
                print("1")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Buy!   Buy!   Buy!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                budget.append(0)
                if WIN[-1]:
                    winsound.PlaySound("buy.wav", winsound.SND_FILENAME)
                #                order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                # Log file
                logfile = open(LOG_FILE_NAME, 'a')
                logfile.write(str(time))
                logfile.write("  buy    price:  %s" % last_price)
                logfile.write("\n")
                logifle.close()
        elif (last_budget == 0):
            if last_price < (current_sell_limit):
                # 2
                print("2")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Sell!   Sell!   Sell!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                budget.append(1)
                if WIN[-1]:
                    winsound.PlaySound("sell.wav", winsound.SND_FILENAME)
                #               order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                # Log file
                logfile = open(LOG_FILE_NAME, 'w')
                logfile.writerow(time.strftime("%Y-%m-%d %H:%M:%S"))
                logfile.write(str(time))
                logfile.write("  buy    price:  %s" % last_price)
                logfile.write("\n")
                logfile.close()
        if (last_price > (current_sell_limit) and last_price < (last_ma)):
            # 3
            print("3")
            print(
                "Almost Sold:              Price = %f,   current_sell_limit = %f" % (last_price, (current_sell_limit)))
            print("Deal GAP:       %f" % abs(almost_order_zone - current_sell_limit))
            if WIN:
                winsound.Beep(500, 1000)
        elif (last_price < current_buy_limit and last_price > last_ma):
            # 4
            print("4")
            print(
                "Almost Buy:               Price = %f,     current_buy_limit = %f" % (last_price, (current_buy_limit)))
            print("Deal GAP:       %f " % abs(current_buy_limit - almost_order_zone))
            if WIN[-1]:
                winsound.Beep(1000, 100)
                winsound.Beep(1000, 100)
        elif (last_price > (current_sell_limit) < BUFFER):
            # 5
            print("5")
            print("Price = %f > MA * %f = %f, No Change" % (last_price, buffer_down, (current_sell_limit)))
        elif (last_price < (current_buy_limit)):
            # 6
            print("6")
            print("Price = %f < MA * %f = %f, No Change" % (last_price, (current_buy_limit)))


ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)

ws.run_forever()
