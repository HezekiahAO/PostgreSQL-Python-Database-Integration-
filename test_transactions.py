"""
test_transactions.py
Integration tests - these run against your REAL bank_transactions database
to confirm insert/retrieve/rollback behavior actually works.

Run with: pytest -v
"""

import pytest
import psycopg2

DB_CONFIG = dict(
    dbname="bank_transactions",
    user="postgres",
    password="YOUR_PASSWORD",
    host="localhost",
    port="5432",
)


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def insert_transaction(conn, transaction):
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
    values = tuple(transaction.values())
    try:
        cur.execute(query, values)
        conn.commit()
    except psycopg2.Error:
        conn.rollback()
        raise
    finally:
        cur.close()


def sample_transaction(tx_id):
    return {
        "transaction_id": tx_id,
        "account_id": "AC00TEST",
        "transaction_amount": 100.00,
        "transaction_date": "2025-01-01 10:00:00",
        "transaction_type": "Debit",
        "location": "TestCity",
        "device_id": "D00TEST",
        "ip_address": "10.0.0.1",
        "merchant_id": "MTEST",
        "channel": "Online",
        "customer_age": 30,
        "customer_occupation": "Tester",
        "transaction_duration": 10,
        "login_attempts": 1,
        "account_balance": 1000.00,
        "previous_transaction_date": "2024-12-01 10:00:00",
    }


@pytest.fixture
def conn():
    connection = get_connection()
    yield connection
    connection.close()


@pytest.fixture
def cleanup_ids():
    """Collects test transaction ids and deletes them after each test."""
    ids = []
    yield ids
    if ids:
        connection = get_connection()
        cur = connection.cursor()
        cur.execute("DELETE FROM transactions WHERE transaction_id = ANY(%s);", (ids,))
        connection.commit()
        cur.close()
        connection.close()


def test_insert_new_transaction(conn, cleanup_ids):
    tx = sample_transaction("TXTEST001")
    cleanup_ids.append(tx["transaction_id"])

    insert_transaction(conn, tx)

    cur = conn.cursor()
    cur.execute("SELECT transaction_id FROM transactions WHERE transaction_id = %s;", (tx["transaction_id"],))
    result = cur.fetchone()
    cur.close()

    assert result is not None
    assert result[0] == "TXTEST001"


def test_duplicate_insert_raises_and_rolls_back(conn, cleanup_ids):
    tx = sample_transaction("TXTEST002")
    cleanup_ids.append(tx["transaction_id"])

    insert_transaction(conn, tx)  # first insert succeeds

    with pytest.raises(psycopg2.Error):
        insert_transaction(conn, tx)  # second insert (duplicate id) should fail

    # confirm only ONE row exists, not a duplicate and not corrupted
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM transactions WHERE transaction_id = %s;", (tx["transaction_id"],))
    count = cur.fetchone()[0]
    cur.close()

    assert count == 1


def test_retrieve_by_account(conn, cleanup_ids):
    tx = sample_transaction("TXTEST003")
    tx["account_id"] = "AC00UNIQUE"
    cleanup_ids.append(tx["transaction_id"])

    insert_transaction(conn, tx)

    cur = conn.cursor()
    cur.execute("SELECT transaction_id FROM transactions WHERE account_id = %s;", ("AC00UNIQUE",))
    rows = cur.fetchall()
    cur.close()

    ids_found = [row[0] for row in rows]
    assert "TXTEST003" in ids_found
