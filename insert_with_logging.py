"""
insert_with_logging.py
Same as insert_with_transaction_handling.py, but now every operation and
error gets written to a log file (db_operations.log) with a timestamp,
instead of just printed to the screen and lost.
"""

import logging
import os
import psycopg2
from dotenv import load_dotenv

# --- Logging setup ---
# This writes to a file AND prints to the console at the same time.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("db_operations.log"),  # saved to disk
        logging.StreamHandler(),                    # also shown in terminal
    ],
)
logger = logging.getLogger(__name__)

conn = psycopg2.connect(
    dbname="bank_transactions",
    user="postgres",
    password=os.environ.get("POSTGRES_PASSWORD"),
    host="localhost",
    port="5432",
)


def insert_transaction(transaction):
    cur = conn.cursor()

    query = """
        INSERT INTO transactions (
            transaction_id, account_id, transaction_amount, transaction_date,
            transaction_type, location, device_id, ip_address, merchant_id,
            channel, customer_age, customer_occupation, transaction_duration,
            login_attempts, account_balance, previous_transaction_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    values = (
        transaction["transaction_id"],
        transaction["account_id"],
        transaction["transaction_amount"],
        transaction["transaction_date"],
        transaction["transaction_type"],
        transaction["location"],
        transaction["device_id"],
        transaction["ip_address"],
        transaction["merchant_id"],
        transaction["channel"],
        transaction["customer_age"],
        transaction["customer_occupation"],
        transaction["transaction_duration"],
        transaction["login_attempts"],
        transaction["account_balance"],
        transaction["previous_transaction_date"],
    )

    try:
        cur.execute(query, values)
        conn.commit()
        logger.info(f"Inserted transaction {transaction['transaction_id']}")
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f"Failed to insert {transaction['transaction_id']}: {e}")
    finally:
        cur.close()


# --- Example usage ---
if __name__ == "__main__":
    insert_transaction({
        "transaction_id": "TX999003",
        "account_id": "AC00999",
        "transaction_amount": 55.00,
        "transaction_date": "2025-01-17 09:00:00",
        "transaction_type": "Debit",
        "location": "Austin",
        "device_id": "D000996",
        "ip_address": "192.168.1.4",
        "merchant_id": "M096",
        "channel": "Online",
        "customer_age": 25,
        "customer_occupation": "Nurse",
        "transaction_duration": 18,
        "login_attempts": 1,
        "account_balance": 2600.00,
        "previous_transaction_date": "2024-09-10 09:00:00",
    })

    # Trigger a logged failure on purpose (duplicate id)
    insert_transaction({
        "transaction_id": "TX999001",  # already exists
        "account_id": "AC00999",
        "transaction_amount": 10.00,
        "transaction_date": "2025-01-17 09:05:00",
        "transaction_type": "Debit",
        "location": "Austin",
        "device_id": "D000995",
        "ip_address": "192.168.1.5",
        "merchant_id": "M095",
        "channel": "Online",
        "customer_age": 25,
        "customer_occupation": "Nurse",
        "transaction_duration": 10,
        "login_attempts": 1,
        "account_balance": 2600.00,
        "previous_transaction_date": "2024-09-10 09:00:00",
    })

    conn.close()
