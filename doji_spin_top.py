"""
Script to identify doji / spinning top formations
"""
from decimal import Decimal
from utils import (is_green_candle, is_red_candle, print_data, get_symbols_data)

EXTRA = Decimal('2.8')

def is_green_doji_spin_top(row):
    body_length = Decimal(row['CLOSE_PRICE']) - Decimal(row['OPEN_PRICE'])
    lower_shadow = Decimal(row['OPEN_PRICE']) - Decimal(row['LOW_PRICE'])
    upper_shadow = Decimal(row['HIGH_PRICE']) - Decimal(row['CLOSE_PRICE'])
    body_length = body_length * EXTRA
    return lower_shadow > body_length and upper_shadow > body_length

def is_red_doji_spin_top(row):
    body_length = Decimal(row['OPEN_PRICE']) - Decimal(row['CLOSE_PRICE'])
    lower_shadow = Decimal(row['CLOSE_PRICE']) - Decimal(row['LOW_PRICE'])
    upper_shadow = Decimal(row['HIGH_PRICE']) - Decimal(row['OPEN_PRICE'])
    body_length = body_length * EXTRA
    return lower_shadow > body_length and upper_shadow > body_length

if __name__ == '__main__':
    doji_spin_top_data = {}
    for row in get_symbols_data():
        if is_green_candle(row) and is_green_doji_spin_top(row):
            doji_spin_top_data.setdefault(row['SERIES'], []).append(row['SYMBOL'])
        elif is_red_candle(row):
            if is_red_doji_spin_top(row):
                doji_spin_top_data.setdefault(row['SERIES'], []).append(row['SYMBOL'])
    print_data(doji_spin_top_data)
