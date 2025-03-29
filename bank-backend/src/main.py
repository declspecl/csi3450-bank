#!/usr/bin/env python

import psycopg2 as pg
from flask_cors import CORS
from flask import Flask, Response, request, jsonify
from queries.bank_queries import get_partial_match_banks_query

app = Flask(__name__)
CORS(app)

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
def get_get_all_banks_query() -> Response:
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
        print("Error executing query: {}".format(e))
        conn.rollback()
        return jsonify([])
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

    return jsonify({
        "banks": [bank.to_json() for bank in banks]
    })
#Adding basic backend setup for people to ensure frontend connection 
# Can change later just needed something running - Stin
@app.route("/people")
def get_people():
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM people")
        rows = cursor.fetchall()
        conn.commit()
    except Exception as e:
        print("Error fetching People")
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
    people = []
    for row in rows:
        people.append({
            "person_id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "birthday": str(row[3]),
            "email": row[4],
            "phone_number": row[5],
            "address": row[6],
            "ssn": row[7],
            "credit_score": row[8]
        })

    return jsonify(people)

if __name__ == "__main__":
<<<<<<< HEAD
    app.run(debug=True)


#Zain testing a push
=======
    app.run(port=8000, debug=True)
<<<<<<< HEAD
>>>>>>> 97356d8d446730f0c227e1a8de126cb9bbe4c315
=======

>>>>>>> 880fc5f70b8468078650e144593d0818d9286212
