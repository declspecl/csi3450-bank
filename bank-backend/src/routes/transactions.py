from server import app, conn
from flask import request, jsonify, Response
from queries.transaction_queries import get_transaction_query, insert_transaction_query

class Transaction:
    def __init__(self, transaction_id: int, amount: float, transaction_date: str, status: str, fk_sender_id: int, fk_recipient_id: int):
        self.transaction_id = transaction_id
        self.amount = amount
        self.transaction_date = transaction_date
        self.status = status
        self.fk_sender_id = fk_sender_id
        self.fk_recipient_id = fk_recipient_id

    def to_json(self) -> dict[str, str | float | int]:
        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "transaction_date": self.transaction_date,
            "status": self.status,
            "fk_sender_id": self.fk_sender_id,
            "fk_recipient_id": self.fk_recipient_id
        }
    
    def __repr__(self) -> str:
        return f"Transaction(transaction_id={self.transaction_id}, amount={self.amount}, transaction_date={self.transaction_date}, status={self.status}, fk_sender_id={self.fk_sender_id}, fk_recipient_id={self.fk_recipient_id})"

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

    transactions: list[Transaction] = []
    for row in transaction_rows:
        print(row)
        transactions.append(Transaction(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5]
        ))

    return jsonify({ "transactions": [transaction.to_json() for transaction in transactions] }), 200


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