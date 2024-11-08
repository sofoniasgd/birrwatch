from app.db import db, init_db
from datetime import datetime
from flask import Flask, jsonify, request, render_template, url_for
from .scheduler import start_scheduler, stop_scheduler
# import the app instance
from app.app_instance import app
from app.scraper.config import bank_url, currency_codes

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
    """Retrieve all exchange rates for a specific date."""
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
    """Retrieve exchange rates for a specific currency across banks."""
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
    """Retrieve the best exchange rates for a specific currency."""
    date = request.args.get('date')  # Optional date filter

    query = ExchangeRates.query.filter_by(currency_code=currency_code)
    if date:
        query = query.filter(ExchangeRates.date == datetime.strptime(date, '%Y-%m-%d').date())
    
    # get the best cash and tx buying and selling rates, skip empty values
    best_cash_buy = query.order_by(ExchangeRates.cash_buy.desc())
    best_cash_sell = query.order_by(ExchangeRates.cash_sell.desc())
    best_tx_buy = query.order_by(ExchangeRates.tx_buy.desc())
    best_tx_sell = query.order_by(ExchangeRates.tx_sell.desc())
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
    """Retrieve exchange rates for a specific bank and currency."""
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
    """Retrieve historical metrics for a specific currency across banks."""
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
@app.route('/api/log_scraping', methods=['POST'])
def log_scraping():
    """Log scraping activity for a bank."""
    data = request.get_json()
    bank_id = data.get('bank_id')
    url = data.get('url')
    success = data.get('success', False)
    next_run = data.get('next_run')

    log_entry = ScrapingLogs(
        bank_id=bank_id,
        url=url,
        run_time=datetime.utcnow(),
        success=success,
        next_run=datetime.strptime(next_run, '%Y-%m-%d %H:%M:%S') if next_run else None
    )
    db.session.add(log_entry)
    db.session.commit()

    return jsonify({"message": "Log entry added successfully"}), 201

# add an endpoint to get all bank names from config.py
@app.route('/api/banks', methods=['GET'])
def get_banks():
    """Retrieve all bank names with IDs."""
    result = []
    for key, value in bank_url.items():
        result.append({"bank_id": key, "name": value['name']})
    return jsonify(result)

# endpoint to get all currencies with their codes
@app.route('/api/currencies', methods=['GET'])
def get_currencies():
    """Retrieve all currencies with their codes."""
    currencies = currency_codes
    return jsonify(currencies)

if __name__ == '__main__':
    app.run(debug=False)