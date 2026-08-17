"""
retrieve_transactions.py
Demonstrates retrieving records using a PARAMETERISED query.

Same idea as insert: the account_id the user searches for is passed in as
a parameter (%s), not glued directly into the SQL string. This means even
if someone searched for something malicious like:
    AC00128'; DROP TABLE transactions; --
...psycopg2 treats it as plain text data, not as part of the SQL command.
That's what "safe from SQL injection" actually means in practice.
"""

import psycopg2

conn = psycopg2.connect(
    dbname="bank_transactions",
    user="postgres",
    password="Hezekiah1!",
    host="localhost",
    port="5432",
)


def get_transactions_by_account(account_id):
    cur = conn.cursor()

    query = """
        SELECT transaction_id, transaction_amount, transaction_date,
               transaction_type, location, channel
        FROM transactions
        WHERE account_id = %s
        ORDER BY transaction_date;
    """

    cur.execute(query, (account_id,))  # note the trailing comma this must be a tuple
    rows = cur.fetchall()
    cur.close()
    return rows


def get_high_value_transactions(min_amount):
    """other example: retrieve all transactions above a given amount."""
    cur = conn.cursor()

    query = """
        SELECT transaction_id, account_id, transaction_amount, transaction_date
        FROM transactions
        WHERE transaction_amount > %s
        ORDER BY transaction_amount DESC;
    """

    cur.execute(query, (min_amount,))
    rows = cur.fetchall()
    cur.close()
    return rows


# --- Example usage ---
if __name__ == "__main__":
    print("Transactions for AC00128:")
    for row in get_transactions_by_account("AC00128"):                                          # Retrives this transaction
        print(row)

    print("\nTop 5 highest-value transactions over $2000:")
    for row in get_high_value_transactions(2000)[:5]:                                           # Retrives the 5 highest transactions over $2000
        print(row)

    conn.close()
