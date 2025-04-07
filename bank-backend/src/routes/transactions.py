from server import app, conn
from flask import request, jsonify, Response
from queries.transaction_queries import get_paginated_transaction_query, insert_transaction_query

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

from queries.transaction_queries import get_paginated_transaction_query

#Paginated and sorted GET request for transactions
@app.route("/transactions", methods=["GET"])
def get_transactions() -> tuple[Response, int]:
    """
    Handles GET requests to retrieve transactions with pagination and optional filters
    """
    cursor = conn.cursor()

    status = request.args.get("status")
    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order", default="ASC")
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=15, type=int)
    limit = page_size
    offset = (page - 1) * page_size

    query, params = get_paginated_transaction_query(
        status=status,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset
    )

    try:
        cursor.execute(query, params)
        transaction_rows = cursor.fetchall()
        conn.commit()
    except Exception as e:
        print(f"Error executing transaction query: {e}")
        conn.rollback()
        return jsonify([]), 500
    finally:
        cursor.close()

    # Count for pagination
    cursor = conn.cursor()
    total_count = 0
    try:
        count_query = "SELECT COUNT(*) FROM transactions WHERE 1=1"
        count_params = []

        if status:
            count_query += " AND status ILIKE %s"
            count_params.append(f"%{status}%")

        cursor.execute(count_query, tuple(count_params))
        count_row = cursor.fetchone()
        if count_row:
            total_count = count_row[0]
    except Exception as e:
        print(f"Error counting transactions: {e}")
        conn.rollback()
        return jsonify([]), 500
    finally:
        cursor.close()

    transactions = [
        Transaction(*row).to_json() for row in transaction_rows
    ]

    return jsonify({
        "transactions": transactions,
        "total_count": total_count
    }), 200


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