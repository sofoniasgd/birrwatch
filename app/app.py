from app.db import db, init_db
from datetime import datetime
from flask import Flask, jsonify, request, render_template, url_for
from flasgger import Swagger
from .scheduler import start_scheduler, stop_scheduler
# import the app instance
from app.app_instance import app
from app.scraper.config import bank_url, currency_codes

# Initialize Swagger
swagger = Swagger(app)

# ===============================
# app = Flask(__name__)

# Configure the MySQL database
# use pymysql bindings
# db_uri = 'mysql+pymysql://at_dev_usr:at_dev_pwd@localhost/birrwatch_db'
# app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init_db(app)
# !!^^^ moved to app_instance.py ^^^!!
# ==============================

# import models for the tables
from .models import ScrapingLogs, ExchangeRates, HistoricalMetrics, BankCurrencies


# !!!!!!!   configure the scheduler   !!!!!!!!!!
# ==============================================
# 
start_scheduler()
#
# ==============================================

# default route, launches the dashboard
@app.route('/', methods=['GET'])
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

# get all exchange rates for a given date
@app.route('/api/exchange_rates', methods=['GET'])
def get_all_exchange_rates():
    """Retrieve all exchange rates for a specific date.
    ---
    parameters:
      - name: date
        in: query
        required: true
        description: 'The date to fetch exchange rates for (format: YYYY-MM-DD).'
        schema:
          type: string
          format: date
    responses:
      200:
        description: A JSON object containing cash and transaction rates.
        content:
          application/json:
            schema:
              type: object
              properties:
                cash_rates:
                  type: array
                  items:
                    type: object
                    properties:
                      bank_id:
                        type: integer
                      currency_code:
                        type: string
                      cash_buy:
                        type: number
                        format: float
                      cash_sell:
                        type: number
                        format: float
                tx_rates:
                  type: array
                  items:
                    type: object
                    properties:
                      bank_id:
                        type: integer
                      currency_code:
                        type: string
                      tx_buy:
                        type: number
                        format: float
                      tx_sell:
                        type: number
                        format: float
      400:
        description: Bad Request - Missing or invalid `date` parameter.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Date parameter is required"
    """
    date = request.args.get('date')

    if not date:
        return jsonify({"error": "Date parameter is required"}), 400

    query = ExchangeRates.query.filter(ExchangeRates.date == datetime.strptime(date, '%Y-%m-%d').date())
    rates = query.all()
    # split the data into cash and tx rates
    # skip empty values
    cash_rates = [
        {
            'bank_id': rate.bank_id,
            'currency_code': rate.currency_code,
            'cash_buy': rate.cash_buy,
            'cash_sell': rate.cash_sell
        } for rate in rates if rate.cash_buy != 0.0
    ]
    tx_rates = [
        {
            'bank_id': rate.bank_id,
            'currency_code': rate.currency_code,
            'tx_buy': rate.tx_buy,
            'tx_sell': rate.tx_sell
        } for rate in rates if rate.tx_buy != 0.0
    ]
    result = {
        'cash_rates': cash_rates,
        'tx_rates': tx_rates
    }
    return jsonify(result)

# get all banks rate for a specific currency
@app.route('/api/banks_rates/<currency_code>', methods=['GET'])
def get_banks_rates(currency_code):
    """Retrieve exchange rates for a specific currency across banks.
    
    This endpoint fetches exchange rates for a specific currency across all 
    available banks. Optionally, a date parameter can be provided to filter 
    the exchange rates for a specific date.
    
    ---
    parameters:
      - name: currency_code
        in: path
        required: true
        description: The currency code (e.g., USD, EUR).
        schema:
          type: string
      - name: date
        in: query
        required: false
        description: 'Optional date filter (format: YYYY-MM-DD).'
        schema:
          type: string
          format: date
    responses:
      200:
        description: A list of exchange rates for the specified currency across banks.
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  bank_id:
                    type: integer
                  cash_buy:
                    type: number
                    format: float
                  cash_sell:
                    type: number
                    format: float
                  tx_buy:
                    type: number
                    format: float
                  tx_sell:
                    type: number
                    format: float
    """
    date = request.args.get('date')  # Optional date filter

    query = ExchangeRates.query.filter_by(currency_code=currency_code)
    if date:
        query = query.filter(ExchangeRates.date == datetime.strptime(date, '%Y-%m-%d').date())
    
    rates = query.all()
    result = [
        {
            'bank_id': rate.bank_id,
            'cash_buy': rate.cash_buy,
            'cash_sell': rate.cash_sell,
            'tx_buy': rate.tx_buy,
            'tx_sell': rate.tx_sell
        } for rate in rates
    ]
    return jsonify(result)

# get the best rates for a specific currency
@app.route('/api/best_rates/<currency_code>', methods=['GET'])
def get_best_rates(currency_code):
    """Retrieve the best exchange rates for a specific currency.

    This endpoint retrieves the best exchange rates (best cash buy, cash sell, 
    transaction buy, and transaction sell) for a specific currency. If no date 
    is provided, today's date is used.
    
    ---
    parameters:
      - name: currency_code
        in: path
        required: true
        description: The currency code (e.g., USD, EUR).
        schema:
          type: string
      - name: date
        in: query
        required: false
        description: 'Optional date filter (format: YYYY-MM-DD).'
        schema:
          type: string
          format: date
    responses:
      200:
        description: The best exchange rates for the specified currency.
        content:
          application/json:
            schema:
              type: object
              properties:
                best_cash_buy:
                  type: object
                  properties:
                    bank_id:
                      type: integer
                    cash_buy:
                      type: number
                      format: float
                best_cash_sell:
                  type: object
                  properties:
                    bank_id:
                      type: integer
                    cash_sell:
                      type: number
                      format: float
                best_tx_buy:
                  type: object
                  properties:
                    bank_id:
                      type: integer
                    tx_buy:
                      type: number
                      format: float
                best_tx_sell:
                  type: object
                  properties:
                    bank_id:
                      type: integer
                    tx_sell:
                      type: number
                      format: float
    """
    date = request.args.get('date')  # Optional date filter or use today

    query = ExchangeRates.query.filter_by(currency_code=currency_code)
    if date:
        query = query.filter(ExchangeRates.date == datetime.strptime(date, '%Y-%m-%d').date())
    else:
        # use current date
        today = datetime.utcnow().date()
        query = query.filter(ExchangeRates.date == today)

    # get the best cash and tx buying and selling rates, skip empty values
    best_cash_buy = query.order_by(ExchangeRates.cash_buy.desc())
    best_cash_sell = query.order_by(ExchangeRates.cash_sell.asc())
    best_tx_buy = query.order_by(ExchangeRates.tx_buy.desc())
    best_tx_sell = query.order_by(ExchangeRates.tx_sell.asc())
    # remove every empty values from each query
    best_cash_buy = best_cash_buy.filter(ExchangeRates.cash_buy != 0.0).first()
    best_cash_sell = best_cash_sell.filter(ExchangeRates.cash_sell != 0.0).first()
    best_tx_buy = best_tx_buy.filter(ExchangeRates.tx_buy != 0.0).first()
    best_tx_sell = best_tx_sell.filter(ExchangeRates.tx_sell != 0.0).first()
    
    result = {
        'best_cash_buy': {
            'bank_id': best_cash_buy.bank_id,
            'cash_buy': best_cash_buy.cash_buy
        },
        'best_cash_sell': {
            'bank_id': best_cash_sell.bank_id,
            'cash_sell': best_cash_sell.cash_sell
        },
        'best_tx_buy': {
            'bank_id': best_tx_buy.bank_id,
            'tx_buy': best_tx_buy.tx_buy
        },
        'best_tx_sell': {
            'bank_id': best_tx_sell.bank_id,
            'tx_sell': best_tx_sell.tx_sell
        }
    }
    return jsonify(result)

# get exchange rates for a specific bank and currency
@app.route('/api/exchange_rates/<bank_id>/<currency_code>', methods=['GET'])
def get_exchange_rates(bank_id, currency_code):
    """Retrieve exchange rates for a specific bank and currency.

    This endpoint retrieves the exchange rates for a given bank and currency.
    Optionally, a date parameter can be provided to filter the rates by date.
    
    ---
    parameters:
      - name: bank_id
        in: path
        required: true
        description: The bank ID.
        schema:
          type: integer
      - name: currency_code
        in: path
        required: true
        description: The currency code (e.g., USD, EUR).
        schema:
          type: string
      - name: date
        in: query
        required: false
        description: 'Optional date filter (format: YYYY-MM-DD).'
        schema:
          type: string
          format: date
    responses:
      200:
        description: A list of exchange rates for the specified bank and currency.
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  date:
                    type: string
                    format: date
                  cash_buy:
                    type: number
                    format: float
                  cash_sell:
                    type: number
                    format: float
                  tx_buy:
                    type: number
                    format: float
                  tx_sell:
                    type: number
                    format: float
    """
    date = request.args.get('date')  # Optional date filter

    query = ExchangeRates.query.filter_by(bank_id=bank_id, currency_code=currency_code)
    if date:
        query = query.filter(ExchangeRates.date == datetime.strptime(date, '%Y-%m-%d').date())
    
    rates = query.all()
    result = [
        {
            'date': rate.date,
            'cash_buy': rate.cash_buy,
            'cash_sell': rate.cash_sell,
            'tx_buy': rate.tx_buy,
            'tx_sell': rate.tx_sell
        } for rate in rates
    ]
    return jsonify(result)

# Fetch Historical Metrics by Currency
@app.route('/api/historical_metrics/<currency_code>', methods=['GET'])
def get_historical_metrics(currency_code):
    """Retrieve historical metrics for a specific currency across banks.

    This endpoint provides historical metrics (e.g., average, max cash rates) 
    for a specified currency. Optional start and end dates can be provided to filter the range.
    
    ---
    parameters:
      - name: currency_code
        in: path
        required: true
        description: The currency code (e.g., USD, EUR).
        schema:
          type: string
      - name: start_date
        in: query
        required: false
        description: 'Optional start date for the historical range (format: YYYY-MM-DD).'
        schema:
          type: string
          format: date
      - name: end_date
        in: query
        required: false
        description: 'Optional end date for the historical range (format: YYYY-MM-DD).'
        schema:
          type: string
          format: date
    responses:
      200:
        description: A list of historical exchange rate metrics.
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  date:
                    type: string
                    format: date
                  avg_cash_buy:
                    type: number
                    format: float
                  avg_cash_sell:
                    type: number
                    format: float
                  max_cash_buy:
                    type: number
                    format: float
                  max_cash_sell:
                    type: number
                    format: float
    """
    start_date = request.args.get('start_date')  # Optional start date filter
    end_date = request.args.get('end_date')      # Optional end date filter

    query = HistoricalMetrics.query.filter_by(currency_code=currency_code)
    if start_date:
        query = query.filter(HistoricalMetrics.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(HistoricalMetrics.date <= datetime.strptime(end_date, '%Y-%m-%d').date())

    metrics = query.all()
    result = [
        {
            'date': metric.date,
            'avg_cash_buy': metric.avg_cash_buy,
            'avg_cash_sell': metric.avg_cash_sell,
            'max_cash_buy': metric.max_cash_buy,
            'max_cash_sell': metric.max_cash_sell
        } for metric in metrics
    ]
    return jsonify(result)

# get Logs of Scraping attempts
@app.route('/api/log_scraping', methods=['GET'])
def log_scraping():
    """Retrieve scraping activity logs for a bank.

    This endpoint fetches all logs related to scraping attempts for different banks, 
    including the success status and the next scheduled scraping time.
    
    ---
    responses:
      200:
        description: A list of scraping activity logs for all banks.
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  bank_id:
                    type: integer
                    description: The ID of the bank.
                  url:
                    type: string
                    description: The URL from which scraping was performed.
                  success:
                    type: boolean
                    description: The success status of the scraping attempt.
                  next_run:
                    type: string
                    format: date-time
                    description: The scheduled next run time for scraping.
      500:
        description: Server error if logs can't be retrieved.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Unable to fetch scraping logs due to a server error."
    """
    logs = ScrapingLogs.query.all()
    result = [
        {
            'bank_id': log.bank_id,
            'url': log.url,
            'success': log.success,
            'next_run': log.next_run
        } for log in logs
    ]
    return jsonify(result)

# add an endpoint to get all bank names from config.py
@app.route('/api/banks', methods=['GET'])
def get_banks():
    """Retrieve all bank names with IDs.

    This endpoint fetches a list of all banks, providing their IDs and names.
    
    ---
    responses:
      200:
        description: A list of banks with their IDs.
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  bank_id:
                    type: integer
                  name:
                    type: string
    """
    result = []
    for key, value in bank_url.items():
        result.append({"bank_id": key, "name": value['name']})
    return jsonify(result)

# endpoint to get all currencies with their codes
@app.route('/api/currencies', methods=['GET'])
def get_currencies():
    """Retrieve all currencies with their codes.

    This endpoint fetches a list of all supported currencies and their respective codes.
    
    ---
    responses:
      200:
        description: A list of currencies with their codes.
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  code:
                    type: string
                  name:
                    type: string
    """
    currencies = currency_codes
    return jsonify(currencies)


if __name__ == '__main__':
    app.run(debug=False)