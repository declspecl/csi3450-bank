from server import app, conn
from flask import request, jsonify, Response
from queries.loan_queries import get_loan_query, insert_loan_query
from datetime import datetime
from typing import Optional

class Loan:
    def __init__(self, loan_id: int, loan_type: str, open_date: datetime, term_length: int, amount: float, status: str, interest_rate: float, fk_person_id: int, fk_bank_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None, bank_name: Optional[str] = None):
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
        self.bank_name = bank_name
    
    def to_json(self) -> dict[str, str | int | float | None]:
        return {
            "loan_id": self.loan_id,
            "type": self.loan_type,
            "open_date": self.open_date.strftime("%Y-%m-%d") if self.open_date else None,
            "term_length": self.term_length,
            "amount": self.amount,
            "status": self.status,
            "interest_rate": self.interest_rate,
            "fk_person_id": self.fk_person_id,
            "fk_bank_id": self.fk_bank_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "bank_name": self.bank_name
        }
    
    def __repr__(self) -> str:
        return f"Loan(loan_id={self.loan_id}, type={self.loan_type}, amount={self.amount}, status={self.status})"

@app.route("/loans", methods=["GET"])
def get_loans() -> tuple[Response, int]:
    """
    Handles GET requests to retrieve loans based on provided parameters.
    Supports filtering by status, person name, bank, interest rate ranges, and loan type.
    Also supports sorting by amount.
    """
    cursor = conn.cursor()
    
    status = request.args.get("status")
    name = request.args.get("name")
    bank_id = request.args.get("bank_id")
    min_interest_rate = request.args.get("min_interest_rate")
    max_interest_rate = request.args.get("max_interest_rate")
    loan_type = request.args.get("loan_type")
    sort_by_amount = request.args.get("sort_by_amount")
    sort_order = request.args.get("sort_order")
    
    query, params = get_loan_query(
        status=status,
        name=name,
        bank_id=int(bank_id) if bank_id else None,
        min_interest_rate=float(min_interest_rate) if min_interest_rate else None,
        max_interest_rate=float(max_interest_rate) if max_interest_rate else None,
        loan_type=loan_type,
        sort_by_amount=bool(sort_by_amount),
        sort_order=sort_order
    )
    
    try:
        cursor.execute(query, params)
        loan_rows = cursor.fetchall()
        conn.commit()
    except Exception as e:
        print(f"Error executing query: {e}")
        conn.rollback()
        return jsonify({"error": "Failed to retrieve loans"}), 500
    finally:
        cursor.close()
    
    loans: list[Loan] = []
    for row in loan_rows:
        loans.append(Loan(
            loan_id=row[0],
            loan_type=row[1],
            open_date=row[2],
            term_length=row[3],
            amount=row[4],
            status=row[5],
            interest_rate=row[6],
            fk_person_id=row[7],
            fk_bank_id=row[8],
            first_name=row[9],
            last_name=row[10],
            bank_name=row[11]
        ))
    
    return jsonify({"loans": [loan.to_json() for loan in loans]}), 200

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
