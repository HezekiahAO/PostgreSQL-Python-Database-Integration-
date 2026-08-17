"""
test_connection.py
Just checks that Python can talk to your bank_transaction database.
Run: python test_connection.py
"""

import psycopg2

conn = psycopg2.connect(
    dbname="bank_transactions",
    user="postgres",
    password="YOUR_PASSWORD",
    host="localhost",
    port="5432",
)

cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM transactions;")
count = cur.fetchone()[0]  # This allows me to grabs exactly one row from your database query results.
print(f"Connected successfully! Row count in transactions table: {count}")

cur.close() # close the execution to free up resources
conn.close() # close the connection 
