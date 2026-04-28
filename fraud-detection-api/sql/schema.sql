CREATE DATABASE IF NOT EXISTS fraud_detection;
USE fraud_detection;

CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    external_id VARCHAR(64) NOT NULL UNIQUE,
    customer_id VARCHAR(64) NOT NULL,
    amount FLOAT NOT NULL,
    currency VARCHAR(8) NOT NULL,
    merchant_name VARCHAR(128) NOT NULL,
    merchant_category VARCHAR(64) NOT NULL,
    payment_channel VARCHAR(32) NOT NULL,
    country VARCHAR(8) NOT NULL,
    card_present BOOLEAN NOT NULL DEFAULT FALSE,
    ip_address VARCHAR(64) NOT NULL,
    device_id VARCHAR(64) NOT NULL,
    transaction_time DATETIME NOT NULL,
    risk_score FLOAT NOT NULL,
    risk_label VARCHAR(16) NOT NULL,
    recommended_action VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL,
    risk_reasons JSON NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
