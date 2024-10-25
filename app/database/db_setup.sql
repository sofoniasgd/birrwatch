-- sets up the database for the project
CREATE TABLE IF NOT EXISTS scraping_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bank_id VARCHAR(4), -- unique bank ID (first four letters of SWIFT)
    url VARCHAR(255),
    run_time DATETIME, -- when the scraping ran
    success BOOLEAN, -- success/failure flag
    next_run DATETIME, -- next scheduled run
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE exchange_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bank_id VARCHAR(4), -- unique bank ID
    currency_code VARCHAR(3), -- currency (e.g., 'USD', 'EUR')
    cash_buy DECIMAL(10, 4), -- cash buying rate
    cash_sell DECIMAL(10, 4), -- cash selling rate
    tx_buy DECIMAL(10, 4), -- transactional buying rate (nullable)
    tx_sell DECIMAL(10, 4), -- transactional selling rate (nullable)
    date DATE, -- date of the exchange rates
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (bank_id, currency_code, date) -- ensure no duplicate records for same bank, currency, and date
);
CREATE TABLE historical_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bank_id VARCHAR(4), -- unique bank ID
    currency_code VARCHAR(3), -- currency (e.g., 'USD', 'EUR')
    date DATE, -- date of the precomputed metric
    avg_cash_buy DECIMAL(10, 4), -- average cash buying rate
    avg_cash_sell DECIMAL(10, 4), -- average cash selling rate
    max_cash_buy DECIMAL(10, 4), -- maximum cash buying rate
    max_cash_sell DECIMAL(10, 4), -- maximum cash selling rate
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- currently the following table is optional
CREATE TABLE bank_currencies (
    bank_id VARCHAR(4),
    currency_code VARCHAR(3),
    PRIMARY KEY (bank_id, currency_code)
);
-- create indexes for often used fields for faster performance
CREATE INDEX idx_exchange_rates ON exchange_rates (bank_id, currency_code, date);
CREATE INDEX idx_scraping_logs ON scraping_logs (bank_id, run_time);
