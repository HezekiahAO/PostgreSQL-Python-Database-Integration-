Week 3 — PostgreSQL & Python Database Integration

A Python application built on top of a PostgreSQL database of bank transactions, demonstrating schema design, parameterised queries, transaction handling, logging, integration tests, and indexing.

Dataset

bank_transactions_data_2.csv — ~2,512 bank transaction records, imported into a transactions table in the bank_transactions database via pgAdmin's Import/Export tool.

1. Setup
Install PostgreSQL and create the database (already done via pgAdmin):
Database name: bank_transactions
Table: transactions (see schema below)
Data imported from bank_transactions_data_2.csv
Create a virtual environment and install dependencies:
bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   pip install psycopg2-binary pytest
In each script, replace PUT_YOUR_PASSWORD_HERE with your PostgreSQL password (or better: set it as an environment variable — see note below).
2. Table schema
sql
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
    customer_age               INTEGER,
    customer_occupation        TEXT,
    transaction_duration       INTEGER,
    login_attempts             INTEGER,
    account_balance            NUMERIC(12,2),
    previous_transaction_date  TIMESTAMP
);
3. Files
File	Purpose
test_connection.py	Confirms Python can connect to the database
insert_transaction.py	Inserts a new transaction using a parameterised query
retrieve_transactions.py	Retrieves transactions by account and by amount, using parameterised queries
insert_with_transaction_handling.py	Same insert, wrapped in try/except with COMMIT on success and ROLLBACK on failure (e.g. duplicate transaction_id)
insert_with_logging.py	Same as above, plus logging of every operation/error to db_operations.log
test_transactions.py	Integration tests (pytest) covering insert, duplicate-rejection/rollback, and retrieval
index_demo.py	Creates an index on account_id and shows the query plan before/after via EXPLAIN ANALYZE
4. Running things
bash
# test the connection
python test_connection.py

# insert a record
python insert_transaction.py

# retrieve records
python retrieve_transactions.py

# see transaction handling (commit/rollback) in action
python insert_with_transaction_handling.py

# see logging in action (check db_operations.log afterward)
python insert_with_logging.py

# run the integration tests
pytest -v

# see the index / EXPLAIN ANALYZE demonstration
python index_demo.py
5. What each task requirement maps to
Requirement	Where
Create DB	bank_transactions database (created in pgAdmin)
Design schema/tables	transactions table (see schema above)
Import sample data	CSV imported via pgAdmin Import/Export tool
Connect Postgres to Python	test_connection.py
Insert/retrieve records	insert_transaction.py, retrieve_transactions.py
Parameterised queries	every query uses %s placeholders, values passed separately
Transaction handling (COMMIT/ROLLBACK)	insert_with_transaction_handling.py
Logging	insert_with_logging.py, writes to db_operations.log
Integration tests	test_transactions.py
Index + EXPLAIN/EXPLAIN ANALYZE	index_demo.py
6. Notes
Passwords are currently hardcoded as placeholders for simplicity during development. In a real deployment these should come from environment variables instead of being committed to source control.
The primary key on transaction_id is what makes duplicate inserts fail — this is what's demonstrated in the rollback example.
The index demo indexes account_id since "find all transactions for one account" is the most common lookup this app performs. With ~2,500 rows, Postgres's query planner may still choose a sequential scan even after the index exists, since it's a small table — that's a legitimate, worth-mentioning observation about cost-based query planning, not a bug.

Personal NOTES:
A parameterised query is a secure way to write database queries by keeping your SQL code separate from user input.