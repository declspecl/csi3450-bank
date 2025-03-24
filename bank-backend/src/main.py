#!/usr/bin/env python

from re import I
import jsonify
import psycopg2 as pg
from flask import Flask, request
from queries import get_partial_match_banks_query

app = Flask(__name__)

DATABASE_NAME="bank"
DATABASE_USER="postgres"
DATABASE_PASSWORD="postgres"
DATABASE_HOST="localhost"
DATABASE_PORT="5432"

conn = pg.connect("dbname={} user={} password={} host={} port={}".format(
    DATABASE_NAME,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT
))

@app.route("/banks")
def get_get_all_banks_query() -> None:
    cursor = conn.cursor()
    name_filter = request.args.get("name")
    location_filter = request.args.get("location")

    query, params = get_partial_match_banks_query(
        name=name_filter if name_filter else "",
        location=location_filter if location_filter else ""
    )

    cursor.execute(query, params)
    banks = cursor.fetchall()

    print(banks)

    cursor.close()
    return None

if __name__ == "__main__":
    app.run(debug=True)
