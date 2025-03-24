#!/usr/bin/env python

import json
import psycopg2 as pg
from flask import Flask, request
from queries.bank_queries import get_partial_match_banks_query

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

class Bank:
    def __init__(self, bank_id: int, name: str, routing_number: int, location: str, phone_number: str):
        self.bank_id = bank_id
        self.name = name
        self.routing_number = routing_number
        self.location = location
        self.phone_number = phone_number

    def __repr__(self) -> str:
        return "Bank(bank_id+{}, name={}, routing_number={}, location={}, phone_number={})".format(
            self.bank_id,
            self.name,
            self.routing_number,
            self.location,
            self.phone_number
        )

    def to_json(self) -> dict[str, str | int]:
        return {
            "bank_id": self.bank_id,
            "name": self.name,
            "routing_number": self.routing_number,
            "location": self.location,
            "phone_number": self.phone_number
        }

@app.route("/banks")
def get_get_all_banks_query() -> str:
    cursor = conn.cursor()

    name = request.args.get("name")
    location = request.args.get("location")

    print("Got request to /banks with params: name={}, location={}".format(name, location))

    query, params = get_partial_match_banks_query(
        name=name,
        location=location
    )

    try:
        cursor.execute(query, params)
        bank_rows = cursor.fetchall()
        conn.commit()
    except Exception as e:
        conn.rollback()
        return json.dumps([])
    finally:
        cursor.close()

    banks: list[Bank] = []
    for bank_row in bank_rows:
        banks.append(Bank(
            int(bank_row[0]),
            bank_row[1],
            int(bank_row[2]),
            bank_row[3],
            bank_row[4]
        ))

    return json.dumps({
        "banks": [bank.to_json() for bank in banks]
    })

if __name__ == "__main__":
    app.run(port=8000, debug=True)
