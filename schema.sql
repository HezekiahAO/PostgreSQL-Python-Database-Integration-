-- schema.sql
-- Did this in pgAdmin

CREATE TABLE transactions (
    transaction_id             TEXT PRIMARY KEY,
    account_id                 TEXT NOT NULL,
    transaction_amount         NUMERIC(10,2) NOT NULL,
    transaction_date           TIMESTAMP NOT NULL,
    transaction_type           TEXT,
    location                   TEXT,
    device_id                  TEXT,
    ip_address                 TEXT,
    merchant_id                TEXT,
    channel                    TEXT,
    customer_age                INTEGER,
    customer_occupation        TEXT,
    transaction_duration       INTEGER,
    login_attempts              INTEGER,
    account_balance            NUMERIC(12,2),
    previous_transaction_date  TIMESTAMP
);

-- My sample data was imported manually into pgAdmin (bank_transactions_data_2.csv)
