"""
Bullish: (Downtrend needs to check manually)
    T-2 day has to be red
    T-1 day has to be green
    T-2 Open has to be less than T-1 Close
    T-2 Close has to be greater than T-1 Open
Bearish: (Uptrend needs to check manually)
    T-2 day has to be green
    T-1 day has to be red
    T-2 Close has to be less than T-1 Open
    T-2 Open has to be greater than T-1 Close
"""
from decimal import Decimal
from utils import (is_green_candle, is_red_candle, print_data, get_symbols_data, symbol_to_record)

def is_bullish_engulf(t1_data, t2_data):
    return (is_green_candle(t1_data) and \
            not is_green_candle(t2_data) and \
            Decimal(t2_data['OPEN_PRICE']) < Decimal(t1_data['CLOSE_PRICE']) and \
            Decimal(t2_data['CLOSE_PRICE']) > Decimal(t1_data['OPEN_PRICE'])
            )

def is_bearish_engulf(t1_data, t2_data):
    return (is_green_candle(t2_data) and \
            not is_green_candle(t1_data) and \
            Decimal(t2_data['CLOSE_PRICE']) < Decimal(t1_data['OPEN_PRICE']) and \
            Decimal(t2_data['OPEN_PRICE']) > Decimal(t1_data['CLOSE_PRICE'])
            )

def is_piercing_pattren(t1_data, t2_data):
    body_length = (Decimal(t2_data['OPEN_PRICE']) - Decimal(t2_data['CLOSE_PRICE'])) / 2
    return (is_red_candle(t2_data) and is_green_candle(t1_data) and \
            Decimal(t2_data['CLOSE_PRICE']) > Decimal(t1_data['OPEN_PRICE']) and \
            Decimal(t1_data['CLOSE_PRICE']) > (Decimal(t2_data['CLOSE_PRICE']) + body_length)
           )

def is_dark_cloud_cover_pattren(t1_data, t2_data):
    body_length = (Decimal(t2_data['CLOSE_PRICE']) - Decimal(t2_data['OPEN_PRICE'])) / 2
    return (is_green_candle(t2_data) and is_red_candle(t1_data) and \
            (Decimal(t1_data['OPEN_PRICE']) > Decimal(t2_data['CLOSE_PRICE'])) and \
            (Decimal(t1_data['CLOSE_PRICE']) < (Decimal(t2_data['OPEN_PRICE']) + body_length))
           )

if __name__ == '__main__':
    bullish_engulf_data = {}
    bearish_engulf_data = {}
    piercing_pattren_data = {}
    dark_cloud_cover_data = {}
    present_day_data = symbol_to_record(get_symbols_data())
    previous_day_data = symbol_to_record(get_symbols_data(filename='T-2-data.csv'))
    for symbol, t1_data in present_day_data.items():
        t2_data = previous_day_data[symbol]
        if is_bullish_engulf(t1_data, t2_data):
            bullish_engulf_data.setdefault(t1_data['SERIES'], []).append(t1_data['SYMBOL'])
        elif is_bearish_engulf(t1_data, t2_data):
            bearish_engulf_data.setdefault(t1_data['SERIES'], []).append(t1_data['SYMBOL'])
        elif is_piercing_pattren(t1_data, t2_data):
            piercing_pattren_data.setdefault(t1_data['SERIES'], []).append(t1_data['SYMBOL'])
        elif is_dark_cloud_cover_pattren(t1_data, t2_data):
            dark_cloud_cover_data.setdefault(t1_data['SERIES'], []).append(t1_data['SYMBOL'])
        else:
            pass
    print "%s BULLISH %s" %("*"*25, "*"*25)
    print_data(bullish_engulf_data)
    print "%s BEARISH %s" %("*"*25, "*"*25)
    print_data(bearish_engulf_data)
    print "%s PIERCING PATTERN %s" %("*"*25, "*"*25)
    print_data(piercing_pattren_data)
    print "%s DARK CLOUD COVER PATTERN %s" %("*"*25, "*"*25)
    print_data(dark_cloud_cover_data)
