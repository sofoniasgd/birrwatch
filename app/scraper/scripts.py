#!/usr/bin/env python
"""Scraping scripts for each bank"""

from bs4 import BeautifulSoup
import requests

def CBET(URL): # API call
    # use Chrome-like headers
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Referrer": "https://combanketh.et/en/exchange-rate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",  # Do Not Track Request Header
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1"
    }
    try:
        # add endpoint, make request and Check if it was successful.
        endpoint = "?_limit=1&_sort=Date%3ADESC&csrt=7354200567639547271"
        url = "{}{}".format(URL, endpoint)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
    # parse data
    data = response.json()
    rates = data[0]["ExchangeRate"]
    print(type(rates))
    for item in rates:
        # get rates and currency code
        code = item["currency"]["CurrencyCode"]
        cashBuying = item["cashBuying"]
        cashSelling = item["cashSelling"]
        tx_buying = item["transactionalBuying"]
        tx_selling = item["transactionalSelling"]
        # store values
        print("{}:\ttxS:{}\ttxB:{}\tCs:{}\tCB:{}".format(code, cashBuying, cashSelling, tx_buying, tx_selling))

def DEET(URL):
    print(URL)

def AWIN(URL):
    print(URL)

def DASH(URL):
    print(URL)

def ABYS(URL):
    print(URL)

def WEGA(URL):
    print(URL)

def UNTD(URL):
    print(URL)

def NIBI(URL):
    print(URL)

def CBOR(URL):
    print(URL)

def LIBS(URL):
    print(URL)

def ORIR(URL):
    print(URL)

def ZEME(URL):
    print(URL)

def BUNA(URL):
    print(URL)

def BERH(URL):
    print(URL)

def ABAY(URL):
    print(URL)

def ABSC(URL):
    print(URL)

def ENAT(URL):
    print(URL)

def DEGA(URL):
    print(URL)

def ZEMZ(URL):
    print(URL)

def GOBT(URL):
    print(URL)

def HIJR(URL):
    print(URL)

def TSCP(URL):
    print(URL)

def AMHR(URL):
    print(URL)

if __name__ == '__main__':
    CBET('https://combanketh.et/cbeapi/daily-exchange-rates')