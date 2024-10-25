from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from .scraper.scraper import script_caller


app = Flask(__name__)

# Configure the MySQL database
# use pymysql bindings
db_uri = 'mysql+pymysql://at_dev_usr:at_dev_pwd@localhost/birrwatch_db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Create the database connection
db = SQLAlchemy(app)

# import models for the tables
from .models import ScrapingLogs, ExchangeRates, HistoricalMetrics, BankCurrencies


# !!!!!!! configure the scheduler !!!!!!!!!!
# ==============================================
scheduler = BackgroundScheduler()

def scheduled_scraping():
    """Function that will be scheduled to run scraping jobs."""
    script_caller()

# Schedule the job to run at 4 AM every day
scheduler.add_job(scheduled_scraping, 'cron', hour=4, minute=0)

# Start the scheduler
scheduler.start()

# Ensure scheduler shuts down with the app
@app.before_first_request
def initialize_scheduler():
    """Starts the scheduler only if it's not already running."""
    if not scheduler.running:
        scheduler.start()

@app.teardown_appcontext
def shutdown_scheduler(exception=None):
    """Shut down the scheduler when the app context ends."""
    scheduler.shutdown(wait=False)
# ==============================================

# get exchange rates
@app.route('/exchange_rates/<bank_id>/<currency_code>', methods=['GET'])
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
@app.route('/historical_metrics/<currency_code>', methods=['GET'])
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

# Log a Scraping attempt
@app.route('/log_scraping', methods=['POST'])
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


if __name__ == '__main__':
    app.run(debug=True)