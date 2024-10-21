#!/usr/bin/env python
"""Web Scraping module
    Handles the data collection and storage to database
"""
from config import bank_url
import scripts

banks_list = ['CBET', 'DEET', 'AWIN', 'DASH', 'ABYS', 'WEGA', 'UNTD', 'NIBI', 'CBOR', 'LIBS', 'ORIR', 'ZEME', 'BUNA', 'BERH', 'ABAY', 'ABSC', 'ENAT', 'DEGA', 'ZEMZ', 'GOBT', 'HIJR', 'TSCP', 'AMHR']

# use config file to fetch the url for each banks website and call subsequent function
for bank_code in banks_list:
    # call each function with it url
    function = getattr(scripts, bank_code)
    link = bank_url[bank_code]["URL"]
    function(link)
# move functions to separate modules

