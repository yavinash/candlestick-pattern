import csv
from decimal import Decimal

ALLOWED_SERIES = ['BE', 'EQ']

def get_nse_500_symbols():
    with open('nifty500.csv', 'r') as data:
        return [row['Symbol'] for row in csv.DictReader(data)]

def get_symbols_data(filename='T-1-data.csv'):
    rows = []
    nse_500 = get_nse_500_symbols()
    with open(filename, 'r') as data:
        rows =  [row for row in csv.DictReader(data) if row['SYMBOL'] in nse_500 and row['SERIES'] in ALLOWED_SERIES]
        # rows =  [row for row in csv.DictReader(data) if row['SERIES'] in ALLOWED_SERIES]
    return rows

def is_green_candle(row):
    return Decimal(row['CLOSE_PRICE']) > Decimal(row['OPEN_PRICE'])

def is_red_candle(row):
    return not is_green_candle(row)

def symbol_to_record(records):
    return dict([(record['SYMBOL'], record) for record in records])

def print_data(data):
    for series, symbols in data.items():
        print '*' * 15
        print series
        print '*' * 15
        for symbol in sorted(symbols):
            print symbol
