from server import app, conn
from flask import request, jsonify, Response
from queries.account_queries import get_account_query, insert_account_query

class Account:
    def __init__(self, account_id: int, account_number: str, routing_number: str, account_type: str, balance: float, status: str, fk_person_id: int, fk_bank_id: int):
        self.account_id = account_id
        self.account_number = account_number
        self.routing_number = routing_number
        self.account_type = account_type
        self.balance = balance
        self.status = status
        self.fk_person_id = fk_person_id
        self.fk_bank_id = fk_bank_id

    def to_json(self) -> dict[str, str | float | int]:
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
    
    def __repr__(self) -> str:
        return f"Account(account_id={self.account_id}, account_number={self.account_number}, routing_number={self.routing_number}, account_type={self.account_type}, balance={self.balance}, status={self.status}, fk_person_id={self.fk_person_id}, fk_bank_id={self.fk_bank_id})"

@app.route("/accounts", methods=["GET"])
def get_accounts() -> tuple[Response, int]:
    """
    Handles GET requests to retrieve account information based on provided parameters    
    """
    cursor = conn.cursor()

    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    account_type = request.args.get("account_type")
    status = request.args.get("status")
    sort_by_balance = request.args.get("sort_by_balance")
    page = request.args.get("page")
    page_size = request.args.get("page_size")

    query, params = get_account_query(
        first_name = first_name,
        last_name = last_name,
        account_type = account_type,
        status = status,
        sort_by_balance = bool(sort_by_balance),
        page = int(page) if page else None,
        page_size = int(page_size) if page_size else None
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

    cursor = conn.cursor()
    total_count = 0
    
    try:
        cursor.execute("SELECT COUNT(*) FROM accounts")
        count_row = cursor.fetchone()
        if count_row:
            total_count = count_row[0]
    except Exception as e:
        print(f"Error executing query: {e}")
        conn.rollback()
        return jsonify([]), 500
    finally:
        cursor.close()

    accounts: list[Account] = []
    for row in account_rows:
        accounts.append(Account(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],    
            row[6],
            row[7]
        ))

    return jsonify({
        "accounts": [account.to_json() for account in accounts],
        "total_count": total_count
    }), 200


@app.route("/accounts", methods=["POST"])
def create_new_account() -> tuple[Response, int]:
    """
    Handles POST requests to insert a new account
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    query, params = insert_account_query(params = data)

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