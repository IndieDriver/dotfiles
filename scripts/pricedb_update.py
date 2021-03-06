#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: pricedb_update.py
Author: indiedriver
Email: arndmathias@gmail.com
Github: https://github.com/indiedriver
Description: Populate beancount price database file with historical price data
"""

import os
import json
import requests
import datetime
import time
import parse

pricedb_path = os.environ['HOME'] + os.sep + ".pricedb"
currencies = {'BTC', 'BCH', 'ETH'}
fiat_symbol = '€'
fiat_query = 'EUR'
start_at = '2018/05/01' # YYYY/MM/DD

def getTimestamp(datetime):
    return str(int(time.mktime(datetime.timetuple())))

def getHistoricalPrice(symbol, fiat, timestamp = ''):
    if timestamp:
        payload = {'fsym': symbol, 'tsyms': fiat, 'ts': timestamp}
    else:
        payload = {'fsym': symbol, 'tsyms': fiat}
    r = requests.get('https://min-api.cryptocompare.com/data/pricehistorical', params=payload);
    data = json.loads(r.text)
    if 'Response' in data:
        print (data);
    return (data[symbol][fiat_query])

def writePriceDatabase(list):
    with open(pricedb_path, "w") as file:
        for entry_list in list:
            file.write(entry_list['date'].strftime("%Y-%m-%d") + " price "
                       + entry_list['symbol'] + " " + entry_list['price'] + " " + entry_list['fiat_symbol'] + "\n")

def queryPrice(dt, cur):
    price = getHistoricalPrice(cur, fiat_query, getTimestamp(dt));
    info = {
        "date": dt,
        "symbol": cur,
        "price":  str(price),
        "fiat_symbol": fiat_query
    }
    return (info)

def main():
    content = []
    parserExp = parse.compile("{date} price {symbol} {value:g} {fiat_symbol}");
    if os.path.exists(pricedb_path):
        with open(pricedb_path, "r") as file:
            for line in file:
                res = parserExp.parse(line);
                dt = datetime.datetime.strptime(res['date'], "%Y-%m-%d")
                info = {
                    "date": dt,
                    "symbol": res['symbol'],
                    "price":  str(res['value']),
                    "fiat_symbol": res['fiat_symbol']
                }
                content.append(info)
    db_content = []
    startDate = datetime.datetime.strptime(start_at, "%Y/%m/%d")
    delta = datetime.datetime.now() - startDate;
    for cur in currencies:
        cur_list = filter(lambda c: c['symbol'] == cur, content)
        for i in range(delta.days + 1):
            dt = startDate + datetime.timedelta(days=i)
            res = list(filter(lambda date: date['date'].date() == dt.date(), cur_list))
            if not res:
                res = queryPrice(dt, cur)
            else:
                res = res[0]
                content.remove(res)
            db_content.append(res)
    for element in content:
        db_content.append(element); # Push remaining elements to final array
    db_content = sorted(db_content, key=lambda k: (k['date'], k['symbol']))
    writePriceDatabase(db_content);

if __name__ == "__main__":
    main()
