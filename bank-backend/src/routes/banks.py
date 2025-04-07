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
#Setting up pagination and filtering for the GET request
@app.route("/banks", methods=["GET"])
def get_banks() -> tuple[Response, int]:
    """
    Handles GET requests to retrieve banks with optional filters and pagination.
    """
    cursor = conn.cursor()

    name = request.args.get("name")
    location = request.args.get("location")
    sort_by = request.args.get("sort_by", default="name")  
    sort_order = request.args.get("sort_order", default="asc")
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=15, type=int)
    limit = page_size
    offset = (page - 1) * page_size

    query, params = get_bank_query(
        name=name,
        location=location,
        limit=limit,
        offset=offset,
        sort_by=sort_by,           
        sort_order=sort_order  
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

    # Re-open cursor to count total rows
    cursor = conn.cursor()
    total_count = 0
    try:
        count_query = "SELECT COUNT(*) FROM banks WHERE 1=1"
        count_params: list[str] = []

        if name:
            count_query += " AND name ILIKE %s"
            count_params.append(f"%{name}%")
        if location:
            count_query += " AND location ILIKE %s"
            count_params.append(f"%{location}%")

        cursor.execute(count_query, tuple(count_params))
        count_row = cursor.fetchone()
        if count_row:
            total_count = count_row[0]
    except Exception as e:
        print(f"Error counting banks: {e}")
        conn.rollback()
        return jsonify({"error": "Failed to count banks"}), 500
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
        "banks": [bank.to_json() for bank in banks],
        "total_count": total_count
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

    name = data.get("name")
    location = data.get("location")
    routing_number = data.get("routing_number")
    phone_number = data.get("phone_number")

    if not all([name, location, routing_number, phone_number]):
        return jsonify({"error": "All fields are required: bank_id, name, location, routing_number, phone_number"}), 400

    query, params = insert_bank_query(
        name=name,
        location=location,
        routing_number=routing_number,
        phone_number=phone_number
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
