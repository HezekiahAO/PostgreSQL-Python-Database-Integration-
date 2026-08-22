"""
index_demo.py
Task 10: create an index and show its effect using EXPLAIN ANALYZE.

We index account_id, since looking up "all transactions for one account"
(what we did in retrieve_transactions.py) is a very common query -
exactly the kind of lookup an index is meant to speed up.
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


conn = psycopg2.connect(
    dbname="bank_transactions",
    user="postgres",
    password=os.environ.get("POSTGRES_PASSWORD"),
    host="localhost",
    port="5432",
)


def explain_account_lookup(account_id="AC00128"):
    cur = conn.cursor()
    cur.execute("EXPLAIN ANALYZE SELECT * FROM transactions WHERE account_id = %s;", (account_id,))
    for row in cur.fetchall():
        print(row[0])
    cur.close()


def create_account_index():
    cur = conn.cursor()
    cur.execute("CREATE INDEX IF NOT EXISTS idx_transactions_account_id ON transactions (account_id);")
    conn.commit()
    cur.close()
    print("Index idx_transactions_account_id created.")


if __name__ == "__main__":
    print("--- EXPLAIN ANALYZE BEFORE index ---")
    explain_account_lookup()

    print("\n--- Creating index ---")
    create_account_index()

    print("\n--- EXPLAIN ANALYZE AFTER index ---")
    explain_account_lookup()

    conn.close()
