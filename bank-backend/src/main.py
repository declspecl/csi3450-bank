#!/usr/bin/env python

from re import I
import jsonify
import psycopg2 as pg
from flask import Flask, request, jsonify
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

    try:
        cursor.execute(query, params)
        banks = cursor.fetchall()
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

    bank_list = []
    for bank in banks:
        bank_list.append({
            "bank_id": bank[0],
            "name": bank[1],
            "routing_number": bank[2],
            "location": bank[3],
            "phone_number": bank[4]
        })

    return jsonify(bank_list)

if __name__ == "__main__":
    app.run(debug=True)
