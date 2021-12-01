"""
Upper shadow diff should be less than 0.2 percent of high
Lower shadow diff should be less than 0.2 percent of Low
Length of candle should be between 1 to 10 percent
"""
from decimal import Decimal
from utils import (is_green_candle, print_data, get_symbols_data)

SHADOW_LENGTH_TO_PRICE = 0.2
BODY_LENGTH = 10

def is_green_candle_length_in_range(row):
    diff = Decimal(row['CLOSE_PRICE']) - Decimal(row['OPEN_PRICE'])
    return 1 < (diff / Decimal(row['OPEN_PRICE'])) * 100 < BODY_LENGTH

def is_green_candle_shadows_in_range(row):
    upper_shadow = ((Decimal(row['HIGH_PRICE']) - Decimal(row['CLOSE_PRICE'])) / Decimal(row['CLOSE_PRICE'])) * 100
    lower_shadow = ((Decimal(row['OPEN_PRICE']) - Decimal(row['LOW_PRICE'])) / Decimal(row['OPEN_PRICE'])) * 100
    return upper_shadow <= SHADOW_LENGTH_TO_PRICE and lower_shadow <= SHADOW_LENGTH_TO_PRICE

def is_red_candle_length_in_range(row):
    diff = Decimal(row['OPEN_PRICE']) - Decimal(row['CLOSE_PRICE'])
    return 1 < (diff / Decimal(row['OPEN_PRICE'])) * 100 < BODY_LENGTH

def is_red_candle_shadows_in_range(row):
    upper_shadow = ((Decimal(row['HIGH_PRICE']) - Decimal(row['OPEN_PRICE'])) / Decimal(row['OPEN_PRICE'])) * 100
    lower_shadow = ((Decimal(row['CLOSE_PRICE']) - Decimal(row['LOW_PRICE'])) / Decimal(row['CLOSE_PRICE'])) * 100
    return upper_shadow <= SHADOW_LENGTH_TO_PRICE and lower_shadow <= SHADOW_LENGTH_TO_PRICE

if __name__ == '__main__':
    bullish_marubozu_data = {}
    bearish_marubozu_data = {}
    for row in get_symbols_data():
        if is_green_candle(row) and is_green_candle_length_in_range(row) and is_green_candle_shadows_in_range(row):
            bullish_marubozu_data.setdefault(row['SERIES'], []).append(row['SYMBOL'])
        else:
            if is_red_candle_length_in_range(row) and is_red_candle_shadows_in_range(row):
                bearish_marubozu_data.setdefault(row['SERIES'], []).append(row['SYMBOL'])
    print "%s BULLISH %s" %("*"*25, "*"*25)
    print_data(bullish_marubozu_data)
    print "%s BEARISH %s" %("*"*25, "*"*25)
    print_data(bearish_marubozu_data)
