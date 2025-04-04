#!/usr/bin/env python

import psycopg2 as pg
from flask_cors import CORS
from flask import Flask, Response, request, jsonify
from queries.bank_queries import get_partial_match_banks_query, insert_bank_query
from queries.person_queries import get_partial_match_person_query, get_paginated_person_query


app = Flask(__name__)
CORS(app)

DATABASE_NAME="bank"
DATABASE_USER="postgres"
DATABASE_PASSWORD="Snowleopard11"
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
    
    #Stin adding type = int to credit_score to ensure it is an integer for filtering
    sort_by_credit_score = request.args.get("credit_score", type = int)
    
    #Stin - Adding sorting--------------------------
    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order", default="ASC")
    #Stin - Adding pagination--------------------------
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=20, type=int)
    limit = page_size
    offset = (page - 1) * page_size
    
    query, params = get_paginated_person_query(
    first_name=first_name,
    last_name=last_name,
    address=address,
    credit_score=sort_by_credit_score,
    sort_by=sort_by,
    sort_order=sort_order,
    limit=limit,
    offset=offset
)#-----------------------------------------------

#commenting out old code as the new code handles pagination and queries
#keeping it for reference
    # print(f"Got request to /person with params: first_name={first_name}, last_name={last_name}, address={address}, credit_score={sort_by_credit_score}")

    # query, params = get_partial_match_person_query(
        # first_name=first_name,
        # last_name=last_name,
        # address=address,
        # credit_score=sort_by_credit_score
    # )

    try:
        cursor.execute(query, params)
        person_rows = cursor.fetchall()
        conn.commit()
        
        #Stin - adding code to get total number of people----------------
        cursor2 = conn.cursor()
        cursor2.execute("SELECT COUNT(*) FROM people")
        total_count = cursor2.fetchone()[0]
        cursor2.close()
        #------------------------------
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
    #Stin- updating return statement to include total number of people
    return jsonify({
        "people": people,
        "total_count": total_count
        }), 200

@app.route("/people", methods=["POST"])
def create_new_person() -> Response:
    """
    Handles POST requests to insert a new person.
    """
    data = request.json
    
    #Stin - removing person_id from params as it is not needed for insertion
    #new_person_id = data.get("person_id")
    new_first_name = data.get("first_name")
    new_last_name = data.get("last_name")
    new_birthday = data.get("birthday")
    new_email = data.get("email")
    new_phone_number = data.get("phone_number")
    new_address = data.get("address")
    new_ssn = data.get("ssn")
    new_credit_score = data.get("credit_score")

    if not all([new_first_name, new_last_name, new_birthday, new_email, new_phone_number, new_address, new_ssn, new_credit_score]):
        return jsonify({"error": "All fields are required: first_name, last_name, birthday, email, phone_number, address, ssn, credit_score"}), 400

    query, params = get_partial_match_person_query(
        insert=True,
        #Stin removing person_id from params as it is not needed for insertion
        #new_person_id=new_person_id,
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
        return jsonify({"message": "✅ Bank inserted successfully!"}), 201
    except Exception as e:
        conn.rollback()
        print(f"Error inserting bank: {e}")
        return jsonify({"error": "Failed to insert bank"}), 500
    finally:
        cursor.close()

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
    people: list[object] = []
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
class Transaction:
    def __init__(self, transaction_id: int, fk_sender_id: str, fk_recipient_id: str, status: str, amount: float, transaction_date: str):
        self.transaction_id = transaction_id
        self.sender = fk_sender_id
        self.recipient = fk_recipient_id
        self.status = status
        self.amount = amount
        self.date = transaction_date

    def to_json(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "status": self.status,
            "amount": self.amount,
            "date": self.date
        }
@app.route("/transactions", methods=["GET"])
def get_transactions():
    """
    Handles GET requests to retrieve transactions.
    """
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT transaction_id, fk_sender_id, fk_recipient_id, status, amount, transaction_date FROM transactions")
        transaction_rows = cursor.fetchall()
        conn.commit()
    except Exception as e:
        print(f"Error executing query: {e}")
        conn.rollback()
        return jsonify({"error": "Failed to retrieve transactions"}), 500
    finally:
        cursor.close()

    transactions = [Transaction(*row).to_json() for row in transaction_rows]

    return jsonify({
        "transactions": transactions
    }), 200

class Account:
    def __init__(self, account_number: str, routing_number: int, account_type: str, balance: float, 
                 status: str, fk_person_id: int, fk_bank_id: int):
        self.account_number = account_number
        self.routing_number = routing_number
        self.account_type = account_type
        self.balance = balance
        self.status = status
        self.fk_person_id = fk_person_id
        self.fk_bank_id = fk_bank_id

    def __repr__(self) -> str:
        return f"Account(account_number={self.account_number}, routing_number={self.routing_number}, " \
               f"account_type={self.account_type}, balance={self.balance}, status={self.status}, " \
               f"fk_person_id={self.fk_person_id}, fk_bank_id={self.fk_bank_id})"

    def to_json(self) -> dict:
        return {
            "account_number": self.account_number,
            "routing_number": self.routing_number,
            "account_type": self.account_type,
            "balance": self.balance,
            "status": self.status,
            "fk_person_id": self.fk_person_id,
            "fk_bank_id": self.fk_bank_id
        }

@app.route("/accounts", methods=["GET"])
def get_accounts() -> tuple[Response, int]:
    """
    Handles GET requests to retrieve accounts with filters if provided.
    """
    
if __name__ == "__main__":
    app.run(port=8000, debug=True)
