"""
insert_with_transaction_handling.py
Same insert as before, but now wrapped in proper transaction handling:
COMMIT on success, ROLLBACK on failure - and the script doesn't crash.

Key idea: a "transaction" in database terms is a group of operations that
either all succeed together, or all fail together. If something goes wrong
partway through, ROLLBACK undoes everything so the database is never left
in a half-finished state.
"""

import os
import psycopg2
from dotenv import load_dotenv

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
        conn.commit()  # success -> save permanently
        print(f"COMMIT - inserted transaction {transaction['transaction_id']}")
    except psycopg2.Error as e:
        conn.rollback()  # failure -> undo, leave database untouched
        print(f"ROLLBACK - could not insert {transaction['transaction_id']}: {e}")
    finally:
        cur.close()


# --- Example usage ---
if __name__ == "__main__":
    # This one is new -> should succeed and COMMIT
    insert_transaction({
        "transaction_id": "TX999002",
        "account_id": "AC00999",
        "transaction_amount": 88.20,
        "transaction_date": "2025-01-16 11:00:00",
        "transaction_type": "Credit",
        "location": "Denver",
        "device_id": "D000998",
        "ip_address": "192.168.1.2",
        "merchant_id": "M098",
        "channel": "ATM",
        "customer_age": 41,
        "customer_occupation": "Teacher",
        "transaction_duration": 30,
        "login_attempts": 1,
        "account_balance": 4200.00,
        "previous_transaction_date": "2024-11-20 09:00:00",
    })

    # This one is TX999001 again (duplicate) -> should fail and ROLLBACK,
    # WITHOUT crashing the script
    insert_transaction({
        "transaction_id": "TX999001",  # duplicate of what we inserted earlier in insert_transaction.py
        "account_id": "AC00999",
        "transaction_amount": 999.99,
        "transaction_date": "2025-01-16 12:00:00",
        "transaction_type": "Debit",
        "location": "Miami",
        "device_id": "D000997",
        "ip_address": "192.168.1.3",
        "merchant_id": "M097",
        "channel": "Online",
        "customer_age": 29,
        "customer_occupation": "Designer",
        "transaction_duration": 20,
        "login_attempts": 1,
        "account_balance": 3100.00,
        "previous_transaction_date": "2024-10-15 09:00:00",
    })

    print("\nScript finished running normally - it did NOT crash.")
    conn.close()
