from server import app, conn
from flask import request, jsonify, Response
from queries.loan_queries import get_paginated_loan_query, insert_loan_query, get_paginated_loan_with_bank_query
from typing import Optional

class Loan:
    def __init__(self, loan_id: int, loan_type: str, open_date: str, term_length: int, amount: float, status: str, interest_rate: float, fk_person_id: int, fk_bank_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None, birthday: Optional[str] = None, email: Optional[str] = None, phone_number: Optional[str] = None, address: Optional[str] = None, ssn: Optional[str] = None, credit_score: Optional[int] = None, bank_name: Optional[str] = None, bank_location: Optional[str] = None, bank_phone_number: Optional[str] = None, bank_routing_number: Optional[str] = None):
        self.loan_id = loan_id
        self.loan_type = loan_type
        self.open_date = open_date
        self.term_length = term_length
        self.amount = amount
        self.status = status
        self.interest_rate = interest_rate
        self.fk_person_id = fk_person_id
        self.fk_bank_id = fk_bank_id
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.ssn = ssn
        self.credit_score = credit_score
        self.bank_name = bank_name
        self.bank_location = bank_location
        self.bank_phone_number = bank_phone_number
        self.bank_routing_number = bank_routing_number
    
    def to_json(self) -> dict[str, str | int | float | None]:
        return {
            "loan_id": self.loan_id,
            "type": self.loan_type,
            "open_date": self.open_date,
            "term_length": self.term_length,
            "amount": self.amount,
            "status": self.status,
            "interest_rate": self.interest_rate,
            "fk_person_id": self.fk_person_id,
            "fk_bank_id": self.fk_bank_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthday": self.birthday,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "ssn": self.ssn,
            "credit_score": self.credit_score,
            "bank_name": self.bank_name,
            "bank_location": self.bank_location,
            "bank_phone_number": self.bank_phone_number,
            "bank_routing_number": self.bank_routing_number
        }
    
    def __repr__(self) -> str:
        return f"Loan(loan_id={self.loan_id}, type={self.loan_type}, amount={self.amount}, status={self.status})"

from queries.loan_queries import get_paginated_loan_query, get_paginated_loan_with_bank_query

@app.route("/loans", methods=["GET"])
def get_loans() -> tuple[Response, int]:
    cursor = conn.cursor()

    # Extract shared query parameters
    status = request.args.get("status")
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    bank_name = request.args.get("bank_name")
    bank_id = request.args.get("bank_id", type=int)
    min_rate = request.args.get("min_interest_rate", type=float)
    max_rate = request.args.get("max_interest_rate", type=float)
    loan_type = request.args.get("loan_type")
    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order", default="ASC")
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=15, type=int)
    limit = page_size
    offset = (page - 1) * page_size
    
    
    bank_name = request.args.get("bank_name")
    bank_location = request.args.get("bank_location")
    bank_phone = request.args.get("bank_phone")


    join_type = request.args.get("join")

    try:
        if join_type == "bank":
            # Use the bank-join-specific query
            query, params = get_paginated_loan_with_bank_query(
                status=status,
                bank_name=bank_name,
                loan_type=loan_type,
                min_interest_rate=min_rate,
                max_interest_rate=max_rate,
                bank_phone=bank_phone,
                bank_location=bank_location,
                sort_by=sort_by,
                sort_order=sort_order,
                limit=limit,
                offset=offset
            )
        else:
            # Default to the normal loan query
            query, params = get_paginated_loan_query(
                status=status,
                first_name=first_name,
                last_name=last_name,
                bank_id=bank_id,
                min_interest_rate=min_rate,
                max_interest_rate=max_rate,
                loan_type=loan_type,
                sort_by=sort_by,
                sort_order=sort_order,
                limit=limit,
                offset=offset
            )

        cursor.execute(query, params)
        loan_rows = cursor.fetchall()
        conn.commit()
    except Exception as e:
        print(f"Error executing loan query: {e}")
        conn.rollback()
        return jsonify({"error": "Failed to retrieve loans"}), 500
    finally:
        cursor.close()

    # ✅ Count query for total rows matching the filters
    count_cursor = conn.cursor()
    try:
        count_query = """
            SELECT COUNT(*)
            FROM loans l
            JOIN people p ON l.fk_person_id = p.person_id
            JOIN banks b ON l.fk_bank_id = b.bank_id
            WHERE 1=1
        """
        count_params = []

        if status:
            count_query += " AND l.status ILIKE %s"
            count_params.append(f"%{status}%")
        if first_name:
            query += " AND p.first_name ILIKE %s"
            params.append(f"%{first_name}%")

        if last_name:   
            query += " AND p.last_name ILIKE %s"
            params.append(f"%{last_name}%")
        if bank_name:
            count_query += " AND b.name ILIKE %s"
            count_params.append(f"%{bank_name}%")
        if bank_location:
            count_query += " AND b.location ILIKE %s"
            count_params.append(f"%{bank_location}%")
        if bank_phone:
            count_query += " AND b.phone_number ILIKE %s"
            count_params.append(f"%{bank_phone}%")
        if bank_id:
            count_query += " AND l.fk_bank_id = %s"
            count_params.append(bank_id)
        if loan_type:
            count_query += " AND l.type ILIKE %s"
            count_params.append(f"%{loan_type}%")
        if min_rate is not None:
            count_query += " AND l.interest_rate >= %s"
            count_params.append(min_rate)
        if max_rate is not None:
            count_query += " AND l.interest_rate <= %s"
            count_params.append(max_rate)

        count_cursor.execute(count_query, count_params)
        total_count = count_cursor.fetchone()[0]
    except Exception as e:
        print(f"Error counting total loans: {e}")
        total_count = 0
    finally:
        count_cursor.close()

    loans = [Loan(*row).to_json() for row in loan_rows]
    return jsonify({"loans": loans, "total_count": total_count}), 200



@app.route("/loans", methods=["POST"])
def create_new_loan() -> tuple[Response, int]:
    """
    Handles POST requests to insert a new loan.
    """
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    loan_type = data.get("type")
    open_date = data.get("open_date")
    term_length = data.get("term_length")
    amount = data.get("amount")
    status = data.get("status")
    interest_rate = data.get("interest_rate")
    fk_person_id = data.get("fk_person_id")
    fk_bank_id = data.get("fk_bank_id")
    
    if not all([loan_type, open_date, term_length, amount, status, interest_rate, fk_person_id, fk_bank_id]):
        return jsonify({"error": "All fields are required: type, open_date, term_length, amount, status, interest_rate, fk_person_id, fk_bank_id"}), 400
    
    try:
        query, params = insert_loan_query({
            "type": loan_type,
            "open_date": open_date,
            "term_length": int(term_length),
            "amount": float(amount),
            "status": status,
            "interest_rate": float(interest_rate),
            "fk_person_id": int(fk_person_id),
            "fk_bank_id": int(fk_bank_id)
        })
        
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return jsonify({"message": "✅ Loan created successfully!"}), 201
        except Exception as e:
            conn.rollback()
            print(f"Error inserting loan: {e}")
            return jsonify({"error": f"Failed to insert loan: {str(e)}"}), 500
        finally:
            cursor.close()
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
