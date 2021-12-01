from decimal import Decimal
from utils import (is_green_candle, print_data, get_symbols_data, symbol_to_record)

def is_bullish_harami(t1_data, t2_data):
    return (is_green_candle(t1_data) and \
            not is_green_candle(t2_data) and \
            Decimal(t1_data['OPEN_PRICE']) > Decimal(t2_data['CLOSE_PRICE']) and \
            Decimal(t1_data['CLOSE_PRICE']) < Decimal(t2_data['OPEN_PRICE'])
            )

def is_bearish_harami(t1_data, t2_data):
    return (is_green_candle(t2_data) and \
            not is_green_candle(t1_data) and \
            Decimal(t1_data['OPEN_PRICE']) < Decimal(t2_data['CLOSE_PRICE']) and \
            Decimal(t1_data['CLOSE_PRICE']) > Decimal(t2_data['OPEN_PRICE'])
            )

if __name__ == '__main__':
    bullish_harami_data = {}
    bearish_harami_data = {}
    present_day_data = symbol_to_record(get_symbols_data())
    previous_day_data = symbol_to_record(get_symbols_data(filename='T-2-data.csv'))
    for symbol, t1_data in present_day_data.items():
        t2_data = previous_day_data[symbol]
        if is_bullish_harami(t1_data, t2_data):
            bullish_harami_data.setdefault(t1_data['SERIES'], []).append(t1_data['SYMBOL'])
        elif is_bearish_harami(t1_data, t2_data):
            bearish_harami_data.setdefault(t1_data['SERIES'], []).append(t1_data['SYMBOL'])
        else:
            pass
    print "%s BULLISH %s" %("*"*25, "*"*25)
    print_data(bullish_harami_data)
    print "%s BEARISH %s" %("*"*25, "*"*25)
    print_data(bearish_harami_data)
