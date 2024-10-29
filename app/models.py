from app.db import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import DECIMAL


# create models for the tables
class ScrapingLogs(db.Model):
    __tablename__ = 'scraping_logs'

    id = db.Column(db.Integer, primary_key=True)
    bank_id = db.Column(db.String(4), nullable=False)  # unique bank ID
    url = db.Column(db.String(255), nullable=True)
    run_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    success = db.Column(db.Boolean, nullable=False)
    next_run = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ScrapingLogs(bank_id='{self.bank_id}', run_time='{self.run_time}', success='{self.success}')>"


class ExchangeRates(db.Model):
    __tablename__ = 'exchange_rates'

    id = db.Column(db.Integer, primary_key=True)
    bank_id = db.Column(db.String(4), nullable=False)  # unique bank ID
    currency_code = db.Column(db.String(3), nullable=False)  # currency code, e.g., 'USD'
    cash_buy = db.Column(DECIMAL(10, 4), nullable=True)  # cash buying rate
    cash_sell = db.Column(DECIMAL(10, 4), nullable=True)  # cash selling rate
    tx_buy = db.Column(DECIMAL(10, 4), nullable=True)  # transactional buying rate
    tx_sell = db.Column(DECIMAL(10, 4), nullable=True)  # transactional selling rate
    date = db.Column(db.Date, nullable=False)  # date of the rate
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('bank_id', 'currency_code', 'date', name='unique_exchange_rate'),)

    def __repr__(self):
        return f"<ExchangeRates(bank_id='{self.bank_id}', currency='{self.currency_code}', date='{self.date}')>"

class HistoricalMetrics(db.Model):
    __tablename__ = 'historical_metrics'

    id = db.Column(db.Integer, primary_key=True)
    bank_id = db.Column(db.String(4), nullable=False)  # unique bank ID
    currency_code = db.Column(db.String(3), nullable=False)  # currency code
    date = db.Column(db.Date, nullable=False)  # date of the precomputed metric
    avg_cash_buy = db.Column(DECIMAL(10, 4), nullable=True)  # average cash buying rate
    avg_cash_sell = db.Column(DECIMAL(10, 4), nullable=True)  # average cash selling rate
    max_cash_buy = db.Column(DECIMAL(10, 4), nullable=True)  # maximum cash buying rate
    max_cash_sell = db.Column(DECIMAL(10, 4), nullable=True)  # maximum cash selling rate
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<HistoricalMetrics(bank_id='{self.bank_id}', currency='{self.currency_code}', date='{self.date}')>"

# optional table for now
class BankCurrencies(db.Model):
    __tablename__ = 'bank_currencies'

    bank_id = db.Column(db.String(4), primary_key=True)
    currency_code = db.Column(db.String(3), primary_key=True)

    def __repr__(self):
        return f"<BankCurrencies(bank_id='{self.bank_id}', currency='{self.currency_code}')>"
