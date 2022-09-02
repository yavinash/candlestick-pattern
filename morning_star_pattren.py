from decimal import Decimal
from utils import (is_green_candle, is_red_candle, print_data, get_symbols_data, symbol_to_record)
from doji_spin_top import (is_green_doji_spin_top, is_red_doji_spin_top)

def is_gap_down_doji(present_day, previous_day):
    return (Decimal(previous_day['CLOSE_PRICE']) > Decimal(present_day['OPEN_PRICE']) and \
            (is_green_doji_spin_top(present_day) if is_green_candle(present_day) else is_red_doji_spin_top(present_day))
           )

def is_morning_star(t1_data, t2_data, t3_data):
    if is_red_candle(t3_data) and is_gap_down_doji(t2_data, t3_data) and is_green_candle(t1_data):
        if is_red_candle(t2_data):
            return Decimal(t1_data['OPEN_PRICE']) > Decimal(t2_data['OPEN_PRICE'])
        else:
            return Decimal(t1_data['OPEN_PRICE']) > Decimal(t2_data['CLOSE_PRICE'])

def get_possible_morning_star_data(t1_data, t2_data, t3_data):
    return ((Decimal(t3_data['LOW_PRICE']) > Decimal(t2_data['LOW_PRICE'])) and \
            is_red_candle(t2_data) and is_gap_down_doji(t1_data, t2_data)
           )

if __name__ == '__main__':
    morning_star_data = {}
    possible_morning_star_data = {}
    present_day_data = symbol_to_record(get_symbols_data())
    previous_day_data = symbol_to_record(get_symbols_data(filename='T-2-data.csv'))
    day_defore_data = symbol_to_record(get_symbols_data(filename='T-3-data.csv'))
    for symbol, t1_data in present_day_data.items():
        try:
            t2_data = previous_day_data[symbol]
            t3_data = day_defore_data[symbol]
        except KeyError:
            continue
        if is_morning_star(t1_data, t2_data, t3_data):
            morning_star_data.setdefault(t1_data['SERIES'], []).append(t1_data['SYMBOL'])
        if get_possible_morning_star_data(t1_data, t2_data, t3_data):
            possible_morning_star_data.setdefault(t1_data['SERIES'], []).append(t1_data['SYMBOL'])
    print "%s Morning Star Formed %s" %("*"*25, "*"*25)
    print_data(morning_star_data)
    print "%s Possible Morning Star %s" %("*"*25, "*"*25)
    print_data(possible_morning_star_data)
