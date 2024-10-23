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
        return
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
        return
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
        return
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
        return
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

def WEGA(URL): # API CALL
    # use Chrome-like headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "origin": "https://www.wegagen.com/",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,am;q=0.7",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
    }
    # transaction and cash rates are in one table
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
        return
    # parse data
    if 'json' in response.headers.get('Content-Type'):
        data = response.json()["data"]
    else:
        print('Response content is not in JSON format.')
    print(type(data))
    for item in data:
        code = item["attributes"]["code"]
        cashBuying = item["attributes"]["buying"]
        cashSelling = item["attributes"]["selling"]
        tx_buying = item["attributes"]["tra_buying"]
        tx_selling = item["attributes"]["tra_selling"]
        # store values
        print("{}:\tCB:{}\tCS:{}\ttxB:{}\ttxS:{}".format(code, cashBuying, cashSelling, tx_buying, tx_selling))

def UNTD(URL): # BeautifulSoup
    try:
        response = requests.get(URL, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
        return
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("table", id="exchange-rate")
    rows = table.find_all("tr")
    # print(table.text)
    for row in rows:
        tds = row.find_all("td")
         # skip empty rows
        if len(tds) == 0:
            continue
        currency = tds[0].text
        code = currency[3:6]
        cashBuying = tds[1].text
        cashSelling = tds[2].text
        print("{}:\tCB:{}\tCS:{}\t".format(code, cashBuying, cashSelling))
    # print(URL)

def NIBI(URL): # BeautifulSoup
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
        return
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("table", class_="ea-advanced-data-table-6b449cce")
    rows = table.tbody.find_all("tr")
    # print(table.text)
    for row in rows:
        tds = row.find_all("td")
         # skip empty rows
        if len(tds) == 0:
            continue
        currency = tds[1].text
        code = currency[0:3]
        cashBuying = tds[2].text
        cashSelling = tds[3].text
        tx_buying = tds[4].text
        tx_selling = tds[5].text
        print("{}:\tCB:{}\tCS:{}\ttxB:{}\ttxS:{}".format(code, cashBuying, cashSelling, tx_buying, tx_selling))

    # print(URL)

def CBOR(URL): # BeautifulSoup
    # this site requires user-agent headers
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,am;q=0.7",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
    }
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
        return
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("table", id="exchange-rates-table")
    rows = table.tbody.find_all("tr")
    # print(table.text)
    for row in rows:
        tds = row.find_all("td")
        # skip empty rows
        if len(tds) == 0:
            continue
        currency = tds[0].text
        code = currency[1:4]
        cashBuying = tds[1].text
        cashSelling = tds[2].text
        tx_buying = tds[3].text
        tx_selling = tds[4].text
        print("{}:\tCB:{}\tCS:{}\ttxB:{}\ttxS:{}".format(code, cashBuying, cashSelling, tx_buying, tx_selling))
    #print(URL)

def LIBS(URL): # BeautifulSoup
    # this site requires user-agent headers
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,am;q=0.7",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
    }
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
        return
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("table")
    rows = table.tbody.find_all("tr")
    # print(table.text)
    # set currency codes
    codes = ["USD", "GBP", "EUR"]
    for row in rows:
        tds = row.find_all("td")
         # skip empty and first two rows
        if len(tds) == 0 or rows.index(row) <= 1:
            continue
        code = codes[rows.index(row) - 2]
        # print(row.text)
        cashBuying = tds[1].text
        cashSelling = tds[2].text
        print("{}:\tCB:{}\tCS:{}".format(code, cashBuying, cashSelling))

def ORIR(URL): # BeautifulSoup
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
        return
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("table")
    rows = table.tbody.find_all("tr")
    # print(table.text)
    for row in rows:
        tds = row.find_all("td")
        # skip empty and first rows
        if len(tds) == 0 or rows.index(row) == 0:
            continue
        # print(row.text)
        currency = tds[0].text
        code = currency[0:4]
        # JPY label has an extra space infront, remove it
        if code == " JPY":
            code = code[1:]
        cashBuying = tds[1].text
        cashSelling = tds[2].text
        #tx_buying = tds[3].text
        #tx_selling = tds[4].text
        print("{}:\tCB:{}\tCS:{}\t".format(code, cashBuying, cashSelling,))

def ZEME(URL): # BeautifulSoup
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
        return
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("table", class_="table currency-exchange-table")
    rows = table.tbody.find_all("tr")
    # print(table.text)
    for row in rows:
        tds = row.find_all("td")
        # skip empty rows
        if len(tds) == 0:
            continue
        # print(row.text)
        currency = tds[0].text.strip()
        code = currency[0:3]
        cashBuying = tds[1].text.strip()
        cashSelling = tds[2].text.strip()
        print("{}:\tCB:{}\tCS:{}\t".format(code, cashBuying, cashSelling,))

def BUNA(URL): # BeautifulSoup
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
        return
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("table", class_="currency-table")
    rows = table.tbody.find_all("tr")
    # print(table.text)
    for row in rows:
        tds = row.find_all("td")
        # skip empty rows
        if len(tds) == 0:
            continue
        currency = tds[0].text
        code = currency[0:3]
        cashBuying = tds[2].text
        cashSelling = tds[3].text
        tx_buying = tds[4].text
        tx_selling = tds[5].text
        print("{}:\tCB:{}\tCS:{}\ttxB:{}\ttxS:{}".format(code, cashBuying, cashSelling, tx_buying, tx_selling))


def BERH(URL): # BeautifulSoup
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
        return
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    # data is in divs and not in a table this time
    data_div = soup.find("div", class_="elementor-element-28165e1")
    rows = data_div.find_all("div", class_="row")
    for row in rows:
        if rows.index(row) == 0 or rows.index(row) > 6:
            continue
        # get column divs(cols)
        cols = row.find_all("div")
        currency = cols[0].text.strip()
        code = currency[2:5]
        cashBuying = cols[1].text.strip()
        cashSelling = cols[2].text.strip()
        print("{}:\tCB:{}\tCS:{}\t".format(code, cashBuying, cashSelling))

def ABAY(URL): # BeautifulSoup
    # transaction and cash rates are in one paginated table
    # so i can extract data without using selenium to make tables visible
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("table", id="tablepress-25")
    rows = table.tbody.find_all("tr")
    # for row in rows:
    #    print(rows.index(row), row.text.strip())
    # first section of table shows cash rates (rows 1-4)
    # while second section(rows 7-13, 17, 20-21) show transactional rates
    for index in range(1, 5):
        tds = rows[index].find_all("td")
        for td in tds:
            print(td.text)
    print("==============")
    # create a row list since some rows dont have data
    row_list = [*range(7,14), 17, 20, 21]
    for index in row_list:
        tds = rows[index].find_all("td")
        for td in tds:
            print(td.text)

def ABSC(URL):# selenium
    # website has anti-bot features so i have to use selenium
    # Path to ChromeDriver executable
    chrome_driver_path = "/usr/bin/chromedriver"

    # Set up the Chrome WebDriver and get url
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(URL)
    # Wait for the page to load the table
    wait = WebDriverWait(driver, 5)
    table = wait.until(EC.presence_of_element_located((By.ID, "tablepress-13")))

    # Get the page source and parse it with BeautifulSoup
    page_html = driver.page_source
    soup = BeautifulSoup(page_html, 'html.parser')
    # get table
    table = soup.find("table", id="tablepress-13")
    # print(table)
    rows = table.tbody.find_all("tr")
    for row in rows:
        tds = row.find_all("td")
        # skip first and empty rows
        if len(tds) == 0 or rows.index(row) == 0:
            continue
        currency = tds[0].text
        code = currency[0:3]
        tx_buying = tds[1].text
        tx_selling = tds[2].text
        cashBuying = tds[4].text
        cashSelling = tds[5].text
        print("{}:\tCB:{}\tCS:{}\ttxB:{}\ttxS:{}".format(code, cashBuying, cashSelling, tx_buying, tx_selling))

def ENAT(URL): # BeautifulSoup
    # transaction and cash rates are in one paginated table
    # so i can extract data without using selenium to make tables visible
    # using row numbers
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("table", id="tablepress-1")
    rows = table.tbody.find_all("tr")
    # table has four columns(1-5) i'm extracting data out of
    # and some rows have empty rates
    # set active rows
    row_list = [*range(1,4), 12, 16, 17]
    for index in row_list:
        tds = rows[index].find_all("td")
        currency = tds[1].text
        code = currency[0:3]
        cashBuying = tds[2].text
        cashSelling = tds[3].text
        tx_buying = tds[4].text
        tx_selling = tds[5].text
        print("{}:\tCB:{}\tCS:{}\ttxB:{}\ttxS:{}".format(code, cashBuying, cashSelling, tx_buying, tx_selling))


def DEGA(URL): # BeautifulSoup
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
        return
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    # find the table using its cointaining div since it has an id
    table = soup.find("table", class_="wptb-preview-table")
    rows = table.tbody.find_all("tr")
    for row in rows:
        tds = row.find_all("td")
        if rows.index(row) == 0:
            continue
        currency = tds[0].text.strip()
        code = currency[0:3]
        cashBuying = tds[1].text.strip()
        cashSelling = tds[2].text.strip()
        print("{}:\tCB:{}\tCS:{}\t".format(code, cashBuying, cashSelling))

def ZEMZ(URL): # BeautifulSoup
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
        return
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    # data is in divs and not in a table this time
    data_div = soup.find("div", class_="elementor-element-2cbffac")
    # setting attribute to get the direct decsendant divs(rows) only
    rows = data_div.find_all("div", recursive=False)
    print(type(rows))
    for row in rows:
        # skip title row
        if rows.index(row) == 0:
            continue
        # rows is an iterator
        cols = row.find_all("div", recursive=False)
        currency = cols[0].text.strip()
        code = currency[0:3]
        cashBuying = cols[1].text.strip()
        cashSelling = cols[2].text.strip()
        tx_buying = cols[3].text.strip()
        tx_selling = cols[4].text.strip()
        print("{}:\tCB:{}\tCS:{}\ttxB:{}\ttxS:{}".format(code, cashBuying, cashSelling, tx_buying, tx_selling))

def GOBT(URL): # BeautifulSoup
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
        return
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    # find the table using its cointaining div since it has a unique class name
    table = soup.find("table", class_="ea-advanced-data-table-6cf83563")
    rows = table.tbody.find_all("tr")
    for row in rows:
        tds = row.find_all("td")
        currency = tds[0].text.strip()
        code = currency[0:3]
        cashBuying = tds[2].text.strip()
        cashSelling = tds[3].text.strip()
        print("{}:\tCB:{}\tCS:{}\t".format(code, cashBuying, cashSelling))

def HIJR(URL): # BeautifulSoup
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching the webpage: {}".format(e))
        return
    # parse data
    soup = BeautifulSoup(response.content, 'html.parser')
    # find the table using its cointaining div since it has a unique class name
    table = soup.find("table")
    rows = table.tbody.find_all("tr")
    for row in rows:
        # !!need to add currency codes here!!
        tds = row.find_all("td")
        currency = tds[0].text
        code = currency[0:3]
        cashBuying = tds[1].text
        cashSelling = tds[2].text
        tx_buying = tds[3].text
        tx_selling = tds[4].text
        print("{}:\tCB:{}\tCS:{}\ttxB:{}\ttxS:{}".format(code, cashBuying, cashSelling, tx_buying, tx_selling))

def TSCP(URL):
    print(URL)

def AMHR(URL):
    print(URL)

if __name__ == '__main__':
    # CBET('https://combanketh.et/cbeapi/daily-exchange-rates')
    # DEET('https://dbe.com.et/')
    # AWIN('https://awashbank.com/exchange-historical/')
    # DASH('https://dashenbanksc.com/daily-exchange-rates/')
    # ABYS('https://www.bankofabyssinia.com/exchange-rate-2/')
    # WEGA('https://weg.back.strapi.wegagen.com/api/exchange-rates?populate=*')
    # UNTD('https://www.hibretbank.com.et/')
    # NIBI('https://www.nibbanksc.com/exchange-rate/')
    # CBOR('https://coopbankoromia.com.et/daily-exchange-rates/')
    # LIBS('https://anbesabank.com/')
    # ORIR('https://www.oromiabank.com/')
    # ZEME('https://www.zemenbank.com/exchange-rates')
    # BUNA('https://bunnabanksc.com/foreign-exchange/')
    # BERH('https://berhanbanksc.com/')
    # ABAY('https://abaybank.com.et/exchange-rates/')
    # ABSC('https://addisbanksc.com/')
    # ENAT('https://www.enatbanksc.com/')
    # DEGA('https://www.globalbankethiopia.com/')
    # ZEMZ('https://zamzambank.com/exchange-rates/todays-exchange-rate/')
    # GOBT('https://www.gohbetbank.com/todays-exchange-rate/')
    HIJR('https://hijra-bank.com/')