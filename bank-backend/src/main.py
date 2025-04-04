#!/usr/bin/env python

import psycopg2 as pg
from flask_cors import CORS
from flask import Flask, Response, request, jsonify
from queries.bank_queries import get_partial_match_banks_query, insert_bank_query
from queries.person_queries import get_partial_match_person_query
from queries.account_queries import get_partial_match_account_query
from queries.transaction_queries import get_partial_match_transaction_query

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

class Person:
    def __init__(self, person_id: int, first_name: str, last_name: str, birthday: str, 
                 email: str, phone_number: str, address: str, ssn: str, credit_score: int):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.ssn = ssn
        self.credit_score = credit_score
        
    def __repr__(self) -> str:
        return f"Person({self.person_id}, {self.first_name}, {self.last_name})"
        
    def to_json(self) -> dict:
        return {
            "person_id": self.person_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthday": self.birthday,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "ssn": self.ssn, 
            "credit_score": self.credit_score
        }
    
class Account:
    def __init__(self, account_id: int, account_number: int, routing_number: int, account_type: str, balance: int, status: str, fk_person_id: int, fk_bank_id: int):
        self.account_id = account_id
        self.account_number = account_number
        self.routing_number = routing_number
        self.account_type = account_type
        self.balance = balance
        self.status = status
        self.fk_person_id = fk_person_id
        self.fk_bank_id = fk_bank_id
    
    def to_json(self) -> dict:
        return {
            "account_id": self.account_id,
            "account_number": self.account_number,
            "routing_number": self.routing_number,
            "account_type": self.account_type,
            "balance": self.balance,
            "status": self.status,
            "fk_person_id": self.fk_person_id,
            "fk_bank_id": self.fk_bank_id
        }

class Transaction:
    def __init__(self, transaction_id: int, amount: int, transaction_date: str, status: str, fk_sender_id: int, fk_recipient_id: int):
        self.transaction_id = transaction_id
        self.amount = amount
        self.trasnaction_date = transaction_date
        self.status = status
        self.fk_sender_id = fk_sender_id
        self.fk_recipient_id = fk_recipient_id

    def to_json(self):
        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "transaction_date": self.transaction_date,
            "status": self.status,
            "fk_sender_id": self.fk_sender_id,
            "fk_recipient_id": self.fk_recipient_id
        }


# The endpoint will handle GET requests to retrieve banks
@app.route("/banks", methods=["GET"])
def get_banks() -> tuple[Response, int]:
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
        return jsonify({"error": "Failed to retrieve banks"}), 500
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
    }), 200

# The endpoint will handle POST requests to insert a new bank
@app.route("/banks", methods=["POST"])
def create_new_bank() -> tuple[Response, int]:
    """
    Handles POST requests to insert a new bank.
    """
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    new_name = data.get("name")
    new_location = data.get("location")
    new_routing_number = data.get("routing_number")
    new_phone_number = data.get("phone_number")

    if not all([new_name, new_location, new_routing_number, new_phone_number]):
        return jsonify({"error": "All fields are required: bank_id, name, location, routing_number, phone_number"}), 400

    query, params = insert_bank_query(
        new_name=new_name,
        new_location=new_location,
        new_routing_number=new_routing_number,
        new_phone_number=new_phone_number,
    )

    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return jsonify({"message": "Bank inserted successfully!"}), 201
    except Exception as e:
        conn.rollback()
        print(f"Error inserting bank: {e}")
        return jsonify({"error": "Failed to insert bank"}), 500
    finally:
        cursor.close()




# POST and GET methods for person route
@app.route("/people", methods=["GET"])
def get_people() -> Response:
    """
    Handles GET requests to retrieve a persons information based on provided paramaters.
    """
    cursor = conn.cursor()


    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    address = request.args.get("address")
    sort_by_credit_score = request.args.get("credit_score")

    print(f"Got request to /person with params: first_name={first_name}, last_name={last_name}, address={address}, credit_score={sort_by_credit_score}")

    query, params = get_partial_match_person_query(
        first_name=first_name,
        last_name=last_name,
        address=address,
        credit_score=sort_by_credit_score
    )

    try:
        cursor.execute(query, params)
        person_rows = cursor.fetchall()
        conn.commit()
    except Exception as e:
        print(f"Error executing query: {e}")
        conn.rollback()
        return jsonify([]), 500
    finally:
        cursor.close()
    people: list[object] = []
    for row in person_rows:
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

    return jsonify({"people": people}), 200

@app.route("/people", methods=["POST"])
def create_new_person() -> Response:
    """
    Handles POST requests to insert a new person.
    """
    data = request.json

    new_person_id = data.get("person_id")
    new_first_name = data.get("first_name")
    new_last_name = data.get("last_name")
    new_birthday = data.get("birthday")
    new_email = data.get("email")
    new_phone_number = data.get("phone_number")
    new_address = data.get("address")
    new_ssn = data.get("ssn")
    new_credit_score = data.get("credit_score")

    if not all([new_person_id, new_first_name, new_last_name, new_birthday, new_email, new_phone_number, new_address, new_ssn, new_credit_score]):
        return jsonify({"error": "All fields are required: person_id, first_name, last_name, birthday, email, phone_number, address, ssn, credit_score"}), 400

    query, params = get_partial_match_person_query(
        insert=True,
        new_person_id=new_person_id,
        new_first_name=new_first_name,
        new_last_name=new_last_name,
        new_birthday=new_birthday,
        new_email=new_email,
        new_phone_number=new_phone_number,
        new_address=new_address,
        new_ssn=new_ssn,
        new_credit_score=new_credit_score
    )

    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return jsonify({"message": "Person inserted successfully!"}), 201
    except Exception as e:
        conn.rollback()
        print(f"Error inserting person: {e}")
        return jsonify({"error": "Failed to insert person"}), 500
    finally:
        cursor.close()


#GET and POST methods for accounts route
@app.route("/accounts", methods=["GET"])
def get_accounts() -> Response:
    """
    Handles GET requests to retrieve account information based on provided parameters    
    """
    cursor = conn.cursor()

    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    account_type = request.args.get("account_type")
    status = request.args.get("status")
    sort_by_balance = request.args.get("sort_by_balance")

    query, params = get_partial_match_person_query(
        first_name = first_name,
        last_name = last_name,
        account_type = account_type,
        status = status,
        sort_by_balance = bool(sort_by_balance)
    )

    try:
        cursor.execute(query, params)
        account_rows = cursor.fetchall()
        conn.commit()
    except Exception as e:
        print(f"Error executing query: {e}")
        conn.rollback()
        return jsonify([]), 500
    finally:
        cursor.close()
    
    account = [
        {
            "account_id": row[0],
            "account_number": row[1],
            "routing_number": row[2],
            "account_type": row[3],
            "balance": row[4],
            "status": row[5],
            "fk_person_id": row[6],
            "fk_bank_id": row[7]
        }
        for row in account_rows
    ]

    return jsonify({"accounts": account}), 200


@app.route("/accounts", methods=["POST"])
def create_new_account() -> Response:
    """
    Handles POST requests to insert a new account
    """
    data = request.json
    query, params = get_partial_match_account_query(insert = True, **data)

    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return jsonify({"Message": "Account inserted successfully!"}), 201
    except Exception as e:
        conn.rollback()
        print(f"Error inserting account: {e}")
        return jsonify({"Error: Failed to insert account"}), 500
    finally:
        cursor.close()


    

#GET and POST methods for transactions route
@app.route("/transactions", methods=["GET"])
def get_transactions() -> Response:
    """
    Hadnles GET requests to retrieve transactions based on provided parameters
    """
    cursor = conn.cursor()

    status = request.args.get("status")
    sort_by_amount = request.args.get("sort_by_amount")
    recent = request.args.get("recent")

    query, params = get_partial_match_transaction_query(
        status = status,
        sort_by_amount = bool(sort_by_amount),
        recent = bool(recent)
    )

    try:
        cursor.execute(query, params)
        transaction_rows = cursor.fetchall()
        conn.commit()
    except Exception as e:
        print(f"Error executing query: {e}")
        conn.rollback()
        return jsonify([]), 500
    finally:
        cursor.close()

    transactions = [
        {
            "transactions_id": row[0],
            "amount": row[1],
            "transaction_date": row[2],
            "status": row[3],
            "fk_sender_id": row[4],
            "fk_recipient_id": row[5]
        }
        for row in transaction_rows
    ]

    return jsonify({"transactions": transactions}), 200


@app.route("/transactions", methods=["POST"])
def create_new_transaction() -> Response:
    """
    Handles POST requests to insert a new transaction
    """
    data = request.json
    query, params = get_partial_match_transaction_query(insert = True, **data)

    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return jsonify({"Message": "Transcation inserted successfully!"}), 201
    except Exception as e:
        conn.rollback()
        print(f"Error inserting transaction: {e}")
        return jsonify({"Error": "Failed to insert transaction"}), 500
    finally:
        cursor.close()




if __name__ == "__main__":
    app.run(port=8000, debug=True)
