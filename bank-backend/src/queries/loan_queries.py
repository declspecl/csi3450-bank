# SQL Schea:
# ```sql
# CREATE TABLE IF NOT EXISTS banks (
#     bank_id SERIAL PRIMARY KEY,
#     name TEXT NOT NULL,
#     routing_number CHAR(9) NOT NULL UNIQUE,
#     location TEXT NOT NULL,
#     phone_number CHAR(14) NOT NULL
# );
# 
# CREATE TABLE IF NOT EXISTS people (
#     person_id SERIAL PRIMARY KEY,
#     first_name TEXT NOT NULL,
#     last_name TEXT NOT NULL,
#     birthday DATE NOT NULL,
#     email TEXT NOT NULL,
#     phone_number CHAR(14) NOT NULL,
#     address TEXT NOT NULL,
#     ssn CHAR(11) NOT NULL,
#     credit_score INTEGER NOT NULL
# );
# 
# CREATE TABLE IF NOT EXISTS accounts (
#     account_id SERIAL PRIMARY KEY,
#     account_number VARCHAR(17) NOT NULL UNIQUE,
#     routing_number CHAR(9) NOT NULL UNIQUE,
#     account_type TEXT NOT NULL,
#     balance NUMERIC NOT NULL DEFAULT 0,
#     status TEXT NOT NULL,
#     fk_person_id INTEGER NOT NULL REFERENCES people(person_id),
#     fk_bank_id INTEGER NOT NULL REFERENCES banks(bank_id)
# );
# 
# CREATE TABLE IF NOT EXISTS transactions (
#     transaction_id SERIAL PRIMARY KEY,
#     amount NUMERIC NOT NULL,
#     transaction_date DATE NOT NULL,
#     status TEXT NOT NULL,
#     fk_sender_id INTEGER NOT NULL REFERENCES accounts(account_id),
#     fk_recipient_id INTEGER NOT NULL REFERENCES accounts(account_id),
#     CONSTRAINT sender_not_recipient CHECK (fk_sender_id <> fk_recipient_id)
# );
# 
# CREATE TABLE IF NOT EXISTS loans (
#     loan_id SERIAL PRIMARY KEY,
#     type TEXT NOT NULL,
#     open_date DATE NOT NULL,
#     term_length INTEGER NOT NULL,
#     amount NUMERIC NOT NULL,
#     status TEXT NOT NULL,
#     interest_rate NUMERIC NOT NULL,
#     fk_person_id INTEGER NOT NULL REFERENCES people(person_id),
#     fk_bank_id INTEGER NOT NULL REFERENCES banks(bank_id)
# );
# ```

from typing import Optional, TypedDict, Unpack, Any

class GetLoanQueryParams(TypedDict):
    status: Optional[str]
    name: Optional[str]
    bank_id: Optional[int]
    min_interest_rate: Optional[float]
    max_interest_rate: Optional[float]
    loan_type: Optional[str]
    sort_by_amount: Optional[bool]
    sort_order: Optional[str]
    
class InsertLoanParams(TypedDict):
    type: str
    open_date: str
    term_length: int
    amount: float
    status: str
    interest_rate: float
    fk_person_id: int
    fk_bank_id: int

def get_loan_query(**kwargs: Unpack[GetLoanQueryParams]) -> tuple[str, tuple[Any, ...]]:
    """
    Retrieves loans based on the provided filters.
    If no filters are provided, retrieves all loans.
    Supports filtering by status, person name, bank, interest rate, and loan type.
    Also supports sorting by amount.
    """
    status = kwargs.get("status")
    name = kwargs.get("name")
    bank_id = kwargs.get("bank_id")
    min_interest_rate = kwargs.get("min_interest_rate")
    max_interest_rate = kwargs.get("max_interest_rate")
    loan_type = kwargs.get("loan_type")
    sort_by_amount = kwargs.get("sort_by_amount", False)
    sort_order = kwargs.get("sort_order", "ASC")
    if sort_order:
        sort_order = sort_order.upper()
    else:
        sort_order = "ASC"
    
    query = """
        SELECT l.loan_id, l.type, l.open_date, l.term_length, l.amount, l.status, 
               l.interest_rate, l.fk_person_id, l.fk_bank_id, 
               p.first_name, p.last_name, b.name as bank_name
        FROM loans l
        JOIN people p ON l.fk_person_id = p.person_id
        JOIN banks b ON l.fk_bank_id = b.bank_id
        WHERE 1=1
    """
    params: list[Any] = []
    
    if status:
        query += " AND l.status ILIKE %s"
        params.append(f"%{status}%")
        
    if name:
        query += " AND (p.first_name ILIKE %s OR p.last_name ILIKE %s)"
        params.append(f"%{name}%")
        params.append(f"%{name}%")
        
    if bank_id:
        query += " AND l.fk_bank_id = %s"
        params.append(bank_id)
        
    if min_interest_rate is not None:
        query += " AND l.interest_rate >= %s"
        params.append(min_interest_rate)
        
    if max_interest_rate is not None:
        query += " AND l.interest_rate <= %s"
        params.append(max_interest_rate)
        
    if loan_type:
        query += " AND l.type ILIKE %s"
        params.append(f"%{loan_type}%")
    
    # Add sorting
    if sort_by_amount:
        query += f" ORDER BY l.amount {sort_order}"
    
    return query, tuple(params)

def insert_loan_query(params: InsertLoanParams) -> tuple[str, tuple[str, str, int, float, str, float, int, int]]:
    """
    Inserts a new loan with the provided information.
    All parameters are required.
    """
    query = """
        INSERT INTO loans (type, open_date, term_length, amount, status, interest_rate, fk_person_id, fk_bank_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (
        params["type"],
        params["open_date"],
        params["term_length"],
        params["amount"],
        params["status"],
        params["interest_rate"],
        params["fk_person_id"],
        params["fk_bank_id"]
    )
    
    return query, values

