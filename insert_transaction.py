"""
insert_transaction.py
Demonstrates inserting a record using a PARAMETERISED query.

Why parameterised? Instead of building SQL by pasting values directly into
the string (which is dangerous - it opens the door to SQL injection), we
use %s placeholders and pass the actual values separately. psycopg2 handles
escaping them safely.
"""

import psycopg2

conn = psycopg2.connect(
    dbname="bank_transactions",
    user="postgres",
    password="Hezekiah1!",
    host="localhost",
    port="5432",
)


def insert_transaction(transaction):
    """
    transaction: A dict with all the fields for one new transaction row.
    Parameterised query implementation
    """
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

    cur.execute(query, values)
    conn.commit()  # save the change permanently
    cur.close()
    print(f"Inserted transaction {transaction['transaction_id']}")


# --- Example usage ---
if __name__ == "__main__":
    new_transaction = {
        "transaction_id": "TX999001",
        "account_id": "AC00999",
        "transaction_amount": 250.75,
        "transaction_date": "2025-01-15 10:30:00",
        "transaction_type": "Debit",
        "location": "Chicago",
        "device_id": "D000999",
        "ip_address": "192.168.1.1",
        "merchant_id": "M099",
        "channel": "Online",
        "customer_age": 34,
        "customer_occupation": "Engineer",
        "transaction_duration": 45,
        "login_attempts": 1,
        "account_balance": 7200.50,
        "previous_transaction_date": "2024-12-01 09:15:00",
    }

    insert_transaction(new_transaction)
    conn.close()
