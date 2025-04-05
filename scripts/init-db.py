#!/usr/bin/env python3

import os
import pandas as pd
import psycopg2 as pg
from psycopg2.extensions import AsIs

def create_connection():
    DATABASE_PORT = 5432
    DATABASE_HOST = "localhost"
    DATABASE_NAME = "bank"
    DATABASE_USER = "postgres"
    DATABASE_PASSWORD = "Snowleopard11"

    print("[.] Connecting to database")

    conn = pg.connect(
        database=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT
    )

    print("[+] Successfully connected to database")
    return conn

def delete_all_tables(conn, cursor):
    print("[.] Deleting all tables")

    cursor.execute("DROP SCHEMA public CASCADE")
    cursor.execute("CREATE SCHEMA public")
    conn.commit()

    print("[+] Successfully deleted all tables")

def create_tables_from_schema(conn, cursor):
    print("[.] Creating tables from database schema")

    with open("../data/schema.sql", "r") as schema_file:
        sql = "".join(schema_file.readlines())
        cursor.execute(sql)
        conn.commit()

    print("[+] Successfully created tables from database schema")

def insert_sample_data(conn, cursor, clear_tables: bool):
    for sample_data_file in sorted(filter(lambda filename: ".csv" in filename, os.listdir("../data"))):
        table_name = sample_data_file[2:-4]
        df = pd.read_csv("../data/{}".format(sample_data_file))

        if clear_tables:
            print("[.] Clearing table '{}'".format(table_name))

            cursor.execute("TRUNCATE {} CASCADE".format(table_name))
            conn.commit()

            print("[+] Successfully cleared table '{}'".format(table_name))

        for _, row in df.iterrows():
            print("[.] Inserting row from '{}' into table '{}'".format(sample_data_file, table_name))

            columns = ",".join(df.columns)
            placeholders = ",".join(["%s"] * len(df.columns))
            
            values = [row[column] for column in df.columns]
            
            query = "INSERT INTO {} ({}) VALUES ({})".format(
                AsIs(table_name),
                AsIs(columns),
                placeholders
            )
            
            cursor.execute(query, values)

    conn.commit()

    print("[+] Successfully inserted all sample data")
    
    # 🔧 Fixing auto-increment sequences for each table
    print("[.] Fixing serial sequences for auto-incremented IDs")
    sequence_fix_sql = '''
        SELECT setval(pg_get_serial_sequence('people', 'person_id'), (SELECT COALESCE(MAX(person_id), 1) FROM people));
        SELECT setval(pg_get_serial_sequence('accounts', 'account_id'), (SELECT COALESCE(MAX(account_id), 1) FROM accounts));
        SELECT setval(pg_get_serial_sequence('banks', 'bank_id'), (SELECT COALESCE(MAX(bank_id), 1) FROM banks));
        SELECT setval(pg_get_serial_sequence('transactions', 'transaction_id'), (SELECT COALESCE(MAX(transaction_id), 1) FROM transactions));
    '''
    cursor.execute(sequence_fix_sql)
    conn.commit()
    print("[+] Serial sequences successfully updated")

def main():
    conn = create_connection()
    cursor = conn.cursor()

    if input("[?] Do you want to create the tables from the database schema? (Y/n) ").strip().lower() != "n":
        if input("[?] Do you want to delete the tables (if they already exist) (Y/n) ").strip().lower() != "n":
            delete_all_tables(conn, cursor)

        create_tables_from_schema(conn, cursor)

    if input("[?] Do you want to insert the sample data? (Y/n) ").strip().lower() != "n":
        clear_tables = input("[?] Do you want to clear the tables before inserting the data? (Y/n) ").strip().lower() != "n"
        insert_sample_data(conn, cursor, clear_tables)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
