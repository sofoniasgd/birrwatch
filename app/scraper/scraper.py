#!/usr/bin/env python
"""Web Scraping module
    Handles the data collection and storage to database
"""

from app.db import db
from app.scraper.config import bank_url
from datetime import datetime
from app.models import ScrapingLogs, ExchangeRates
from . import scripts

banks_list = ['CBET', 'DEET', 'AWIN', 'DASH', 'ABYS', 'WEGA', 'UNTD', 'NIBI',\
                'CBOR', 'LIBS', 'ORIR', 'ZEME', 'BUNA', 'BERH', 'ABAY', 'ABSC',\
                'ENAT', 'DEGA', 'ZEMZ', 'GOBT', 'HIJR', 'TSCP', 'AMHR']
def script_caller():
    """ main scraping function.
        calls all scraping functions, collects data,
        and stores in database
    """
    # use config file to fetch the url for each banks website
    # and call subsequent function
    for bank_code in banks_list:
        index = banks_list.index(bank_code)
        print("|| Executing script {} of {} code: {} ||".format(index, len(banks_list), bank_code))
        # call each function with it url
        function = getattr(scripts, bank_code)
        link = bank_url[bank_code]["URL"]
        # wrap in try clause to catch any errors
        # either store fetch error data(log) or store fetched data
        try:
            status = function(link)
        except Exception as e:
            # log failed scraping attempt
            log_entry = ScrapingLogs(
                bank_id=bank_code,
                url=link,
                run_time=datetime.now(),
                success=False,
                next_run=datetime.now()
            )
            db.session.add(log_entry)
            print("ERROR: ", e)
        # extract data when no errors occured
        else:
            # status will return a dict with exchage data
            data = status["data"]
            # data is a list of dict entries
            # entry: bankid, currency, csbuying, cselling, tbuying, tsellingg
            for rate in data:
                single_rate = ExchangeRates(
                    bank_id = bank_code,
                    currency_code = rate['currency'],
                    cash_buy = rate['cash_buying'],
                    cash_sell = rate['cash_selling'],
                    tx_buy = rate['transactional_buying'],
                    tx_sell = rate['transactional_selling'],
                    date = datetime.now().date(),
                    created_at = datetime.now()
                )
                db.session.add(single_rate)
        # put a commit here to ensure that either all records are stored
        # or failure logs are stored
        # put commit code ina try catch to not propagate errors
        finally:
            try:
                db.session.commit()
                print(f"Successfully added {len(data)} records.")
            except Exception as e:
                # Rollback if there's an error
                db.session.rollback() 
                print(f"Error occurred while adding records: {e}")
            
    # close the session
    db.session.close()


