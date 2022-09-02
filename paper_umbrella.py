"""
Upper shadow should not present
Lower shadow has to be more than double of ength of body
"""
from decimal import Decimal
from utils import (is_green_candle, print_data, get_symbols_data)

def is_small_green_upper_shadow(row):
    upper_shadow = ((Decimal(row['HIGH_PRICE']) - Decimal(row['CLOSE_PRICE'])) / Decimal(row['CLOSE_PRICE'])) * 100
    return upper_shadow <= 0.2

def is_green_lower_shadow_bigger(row):
    body_length = Decimal(row['CLOSE_PRICE']) - Decimal(row['OPEN_PRICE'])
    lower_shadow_length = Decimal(row['OPEN_PRICE']) - Decimal(row['LOW_PRICE'])
    return (lower_shadow_length - (body_length * 2)) > 0

def is_small_red_upper_shadow(row):
    upper_shadow = ((Decimal(row['HIGH_PRICE']) - Decimal(row['OPEN_PRICE'])) / Decimal(row['OPEN_PRICE'])) * 100
    return upper_shadow <= 0.2

def is_red_lower_shadow_bigger(row):
    body_length = Decimal(row['OPEN_PRICE']) - Decimal(row['CLOSE_PRICE'])
    lower_shadow_length = Decimal(row['CLOSE_PRICE']) - Decimal(row['LOW_PRICE'])
    return (lower_shadow_length - (body_length * 2)) > 0

if __name__ == '__main__':
    paper_umbrella_data = {}
    for row in get_symbols_data():
        if is_green_candle(row) and is_small_green_upper_shadow(row) and is_green_lower_shadow_bigger(row):
            paper_umbrella_data.setdefault(row['SERIES'], []).append(row['SYMBOL'])
        else:
            if is_small_red_upper_shadow(row) and is_red_lower_shadow_bigger(row):
                paper_umbrella_data.setdefault(row['SERIES'], []).append(row['SYMBOL'])
    print_data(paper_umbrella_data)
