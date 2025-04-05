from server import app, conn
from flask import request, jsonify, Response
from queries.bank_queries import get_bank_query, insert_bank_query

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

    query, params = get_bank_query(
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
        return jsonify({"message": "✅ Bank inserted successfully!"}), 201
    except Exception as e:
        conn.rollback()
        print(f"Error inserting bank: {e}")
        return jsonify({"error": "Failed to insert bank"}), 500
    finally:
        cursor.close()
