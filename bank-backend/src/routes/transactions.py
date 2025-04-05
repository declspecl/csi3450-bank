from server import app, conn
from flask import request, jsonify, Response
from queries.transaction_queries import get_transaction_query, insert_transaction_query

class Transaction:
    def __init__(self, transaction_id: int, fk_sender_id: str, fk_recipient_id: str, status: str, amount: float, transaction_date: str):
        self.transaction_id = transaction_id
        self.sender = fk_sender_id
        self.recipient = fk_recipient_id
        self.status = status
        self.amount = amount
        self.date = transaction_date

    def to_json(self) -> dict[str, str | float | int]:
        return {
            "transaction_id": self.transaction_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "status": self.status,
            "amount": self.amount,
            "date": self.date
        }

#GET and POST methods for transactions route
@app.route("/transactions", methods=["GET"])
def get_transactions() -> tuple[Response, int]:
    """
    Hadnles GET requests to retrieve transactions based on provided parameters
    """
    cursor = conn.cursor()

    status = request.args.get("status")
    sort_by_amount = request.args.get("sort_by_amount")
    recent = request.args.get("recent")

    query, params = get_transaction_query(
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
def create_new_transaction() -> tuple[Response, int]:
    """
    Handles POST requests to insert a new transaction
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    query, params = insert_transaction_query(params = data)

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