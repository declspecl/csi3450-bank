from server import app, conn
from flask import request, jsonify, Response
from queries.account_queries import get_account_query, insert_account_query

#GET and POST methods for accounts route
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

    query, params = get_account_query(
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