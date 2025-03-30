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

# POST and GET for inserting and retrieving banks
# The endpoint will handle both GET requests to retrieve banks and POST requests to insert a new bank
@app.route("/banks", methods=["GET"])
def get_banks() -> Response:
    """
    Handles GET requests to retrieve banks based on name and location.
    """
    cursor = conn.cursor()

    name = request.args.get("name")
    location = request.args.get("location")

    print(f"Got request to /banks with params: name={name}, location={location}")

    query, params = get_partial_match_banks_query(
        name=name,
        location=location
    )

    try:
        cursor.execute(query, params)
        bank_rows = cursor.fetchall()
        conn.commit()
    except Exception as e:
        print(f"Error executing query: {e}")
        conn.rollback()
        return jsonify([]), 500
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


@app.route("/banks", methods=["POST"])
def create_new_bank() -> Response:
    """
    Handles POST requests to insert a new bank.
    """
    data = request.json

    new_bankid = data.get("bank_id")
    new_name = data.get("name")
    new_location = data.get("location")
    new_routing_number = data.get("routing_number")
    new_phone_number = data.get("phone_number")

    if not all([new_bankid, new_name, new_location, new_routing_number, new_phone_number]):
        return jsonify({"error": "All fields are required: bank_id, name, location, routing_number, phone_number"}), 400

    query, params = get_partial_match_banks_query(
        insert=True,
        new_bankid=new_bankid,
        new_name=new_name,
        new_location=new_location,
        new_routing_number=new_routing_number,
        new_phone_number=new_phone_number,
    )

    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return jsonify({"message": "✅ Bank inserted successfully!"}), 201
    except Exception as e:
        conn.rollback()
        print(f"Error inserting bank: {e}")
        return jsonify({"error": "Failed to insert bank"}), 500
    finally:
        cursor.close()

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
        print(f"Error inserting bank: {e}")  # <-- Add this to print the exact error
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
    app.run(port=8000, debug=True)

