#!/usr/bin/env python
"""Scraping scripts for each bank"""

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        print("{}:\tCB:{}\tCS:{}\ttxB:{}\ttxS:{}".format(code, cashBuying, cashSelling, tx_buying, tx_selling))

def DEET(URL): # selenium
    # since the table has a selector for how many rows to show
    # i have to use selenium here to interact with the table
    # to show the maximum number of results

    # Path to ChromeDriver executable
    chrome_driver_path = "/usr/bin/chromedriver"

    # Set up the Chrome WebDriver and get url
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(URL)
    # Wait for the dropdown to be present
    wait = WebDriverWait(driver, 5)
    dropdown_element = wait.until(EC.presence_of_element_located((By.NAME, "tablepress-1_length")))
    
    select = Select(dropdown_element)
    # Select an option by value
    select.select_by_value("50")
    dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "tablepress-1")))
    # Get the page source and parse it with BeautifulSoup
    page_html = driver.page_source
    soup = BeautifulSoup(page_html, 'html.parser')
    # get table
    table = soup.find("table", id="tablepress-1")
    # print(table)
    rows = table.tbody.find_all("tr")

    for row in rows:
        code = row.find("td", class_="column-2").text
        cashBuying = row.find("td", class_="column-3").text
        cashSelling = row.find("td", class_="column-4").text
        
        print("{}:\tCB:{}\tCS:{}".format(code, cashBuying, cashSelling))


def AWIN(URL): # BeautifulSoup
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("table", id="exchange-rates-table")
    rows = table.tbody.find_all("tr")

    for row in rows:
        tds = row.find_all("td")
        currency = tds[0].text
        code = currency[1:4]
        cashBuying = tds[1].text
        cashSelling = tds[2].text
        tx_buying = tds[3].text
        tx_selling = tds[4].text
        print("{}:\tCB:{}\tCS:{}\ttxB:{}\ttxS:{}".format(code, cashBuying, cashSelling, tx_buying, tx_selling))

def DASH(URL): # BeautifulSoup
    # transaction and cash rates are in two tables and made visible by css
    # so i can extract data without using selenium to make tables visible
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all("table")
    # get data for each table
    for table in tables:
        first_row = table.tbody.find_all("tr")[0]
        rate_type = first_row.find_all("td")[2]
        rows = table.tbody.find_all("tr")
        # print(rate_type.text)
        for row in rows:
            tds = row.find_all("td")
            currency = tds[0].text
            code = currency[1:4]
            # depending on the rate_type store in corresponding variable
            if rate_type.text == "Cash Buying":
                cashBuying = tds[2].text
                cashSelling = tds[3].text
                print("{}:\tCB:{}\tCS:{}\t".format(code, cashBuying, cashSelling))
            else:
                tx_buying = tds[2].text
                tx_selling = tds[2].text
                print("{}:\ttxB:{}\ttxS:{}".format(code, tx_buying, tx_selling))

def ABYS(URL): # BeautifulSoup
    # transaction and cash rates are in one paginated table
    # so i can extract data without using selenium to make tables visible
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("table", id="tablepress-15")
    rows = table.tbody.find_all("tr")
    # first section of table shows cash rates (rows 2-11)
    # while second section(rows 14-31) show transactional rates
    for index in range(2, 12):
        tds = rows[index].find_all("td")
        for td in tds:
            print(td.text)
    print("==============")
    for index in range(14, 32):
        tds = rows[index].find_all("td")
        for td in tds:
            print(td.text)

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
    # CBET('https://combanketh.et/cbeapi/daily-exchange-rates')
    # DEET('https://dbe.com.et/')
    # AWIN('https://awashbank.com/exchange-historical/')
    # DASH('https://dashenbanksc.com/daily-exchange-rates/')
    ABYS('https://www.bankofabyssinia.com/exchange-rate-2/')