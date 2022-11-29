import urllib
import time
import csv
import requests
from decimal import Decimal
from bs4 import BeautifulSoup
from io import StringIO
from pprint import pprint


headers = {"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
"Cache-Control": "no-cache", "Connection": "keep-alive", "Host": "www1.nseindia.com", "Pragma": "no-cache", "Referer": "https://www1.nseindia.com/products/content/equities/equities/eq_security.htm", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36", "X-Requested-With": "XMLHttpRequest"}


def get_symbol_count(symbol):
    url = 'https://www1.nseindia.com/marketinfo/sym_map/symbolCount.jsp?symbol=%s' % (symbol)
    page = requests.get(url, headers=headers)
    content = page.content.strip()
    return content


def get_close_prices(symbol):
    close_price_data = {}
    symbol_count = int(get_symbol_count(symbol))
    quote_symbol = urllib.parse.quote(symbol)
    url = f'https://www1.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol={quote_symbol}&segmentLink=3&symbolCount={symbol_count}&series=ALL&dateRange=24month&fromDate=&toDate=&dataType=PRICEVOLUMEDELIVERABLE'
    # url = f'https://www1.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol={quote_symbol}&segmentLink=3&symbolCount={symbol_count}&series=ALL&dateRange=+&fromDate=01-11-2021&toDate=31-10-2022&dataType=PRICEVOLUMEDELIVERABLE'
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    data = soup.find(id='csvContentDiv').text
    data = [row for row in csv.reader(StringIO(data), delimiter=':', quoting=csv.QUOTE_NONE)][0]
    for day in data[1:]:
        if not day.strip():
            continue
        day = [row for row in csv.reader(StringIO(day), delimiter=',', quoting=csv.QUOTE_ALL)][0]
        day = [elem.strip() for elem in day]
        if day[1] not in ['EQ', 'BE']:
            continue
        close_price_data[day[2]] = day[8]
    return close_price_data


def get_nse_500_symbols():
    with open('data.csv', 'r') as data:
        return [row['Symbol'] for row in csv.DictReader(data)]


def get_all_symbol_data():
    symbol_data = {}
    fields = ['Symbol']
    symbols = get_nse_500_symbols()
    for ind, symbol in enumerate(symbols):
        data = get_close_prices(symbol)
        for date, close_price in data.items():
            if ind == 0:
                fields.append(date)
            symbol_data.setdefault(symbol, {}).update({'Symbol': symbol, date: close_price})
    with open('organised-data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        for date, data in symbol_data.items():
            writer.writerow(data)


get_all_symbol_data()
