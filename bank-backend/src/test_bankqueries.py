import psycopg2

from queries.bank_queries import (
    get_get_all_banks_query,
    filter_banks_by_name,
    filter_banks_by_location
)

# Establish a connection to your PostgreSQL database
conn = psycopg2.connect(
    dbname="bank",
    user="postgres",
    password="postgres",
    host="localhost"
)
cur = conn.cursor()

# Test: Get all banks
query = get_get_all_banks_query()
cur.execute(query)
banks = cur.fetchall()
print("All Banks:", banks)

# Test: Filter banks by name
query, params = filter_banks_by_name("Chase")
cur.execute(query, params)
banks_by_name = cur.fetchall()
print("Banks with 'Chase' in the name:", banks_by_name)

# Test: Filter banks by location
query, params = filter_banks_by_location("New York")
cur.execute(query, params)
banks_by_location = cur.fetchall()
print("Banks located in New York:", banks_by_location)

# Cleanup: Close the cursor and connection
cur.close()
conn.close()
