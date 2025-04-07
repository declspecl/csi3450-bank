from server import app, conn
from flask import request, jsonify, Response
from queries.account_queries import get_paginated_account_query, insert_account_query

class Account:
    def __init__(self, account_id: int, account_number: str, routing_number: str,
                 account_type: str, balance: float, status: str,
                 fk_person_id: int, fk_bank_id: int, bank_name: str = None):
        self.account_id = account_id
        self.account_number = account_number
        self.routing_number = routing_number
        self.account_type = account_type
        self.balance = balance
        self.status = status
        self.fk_person_id = fk_person_id
        self.fk_bank_id = fk_bank_id
        self.bank_name = bank_name

    def to_json(self) -> dict[str, str | float | int]:
        result = {
            "account_id": self.account_id,
            "account_number": self.account_number,
            "routing_number": self.routing_number,
            "account_type": self.account_type,
            "balance": self.balance,
            "status": self.status,
            "fk_person_id": self.fk_person_id,
            "fk_bank_id": self.fk_bank_id
        }
        if self.bank_name:
            result["bank_name"] = self.bank_name
        return result

    def __repr__(self) -> str:
        return (
            f"Account(account_id={self.account_id}, account_number={self.account_number}, "
            f"routing_number={self.routing_number}, account_type={self.account_type}, "
            f"balance={self.balance}, status={self.status}, fk_person_id={self.fk_person_id}, "
            f"fk_bank_id={self.fk_bank_id}, bank_name={self.bank_name})"
        )

#Swapped functions from get_account_query to get_paginated_account_query to work with pagination and sorting
@app.route("/accounts", methods=["GET"])
def get_accounts() -> tuple[Response, int]:
    """
    Handles GET requests to retrieve account information with pagination, filtering, and sorting
    """
    cursor = conn.cursor()

    fk_person_id = request.args.get("fk_person_id", type=int)
    account_type = request.args.get("account_type")
    status = request.args.get("status")
    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order", default="ASC")
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=20, type=int)
    limit = page_size
    offset = (page - 1) * page_size

    query, params = get_paginated_account_query(
        fk_person_id=fk_person_id,
        account_type=account_type,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset
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
        print(f"Error counting accounts: {e}")
        conn.rollback()
        return jsonify([]), 500
    finally:
        cursor.close()

    accounts: list[Account] = []
    for row in account_rows:
        # Adjust index mapping if SELECT changes
        accounts.append(Account(
            account_id=0,  
            account_number=row[0],
            routing_number=row[1],
            account_type=row[2],
            balance=row[3],
            status=row[4],
            fk_person_id=row[5],
            fk_bank_id=row[6],
            bank_name=row[7] #bank name
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