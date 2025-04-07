from typing import Optional, TypedDict, Unpack, Any

class GetLoanQueryParams(TypedDict):
    status: Optional[str]
    name: Optional[str]
    bank_id: Optional[int]
    min_interest_rate: Optional[float]
    max_interest_rate: Optional[float]
    loan_type: Optional[str]
    sort_by: Optional[str]
    sort_order: Optional[str]
    limit: Optional[int]
    offset: Optional[int]
    
class InsertLoanParams(TypedDict):
    type: str
    open_date: str
    term_length: int
    amount: float
    status: str
    interest_rate: float
    fk_person_id: int
    fk_bank_id: int

def get_paginated_loan_query(**kwargs: Unpack[GetLoanQueryParams]) -> tuple[str, tuple[Any, ...]]:
    """
    Retrieves loans based on the provided filters.
    If no filters are provided, retrieves all loans.
    Supports filtering by status, person name, bank, interest rate, and loan type.
    Also supports sorting by amount.
    """
    status = kwargs.get("status")
    first_name = kwargs.get("first_name")
    last_name = kwargs.get("last_name")
    bank_id = kwargs.get("bank_id")
    min_interest_rate = kwargs.get("min_interest_rate")
    max_interest_rate = kwargs.get("max_interest_rate")
    loan_type = kwargs.get("loan_type")
    sort_order = kwargs.get("sort_order", "ASC")
    if sort_order:
        sort_order = sort_order.upper()
    else:
        sort_order = "ASC"
    
    query = """
        SELECT l.loan_id, l.type, l.open_date, l.term_length, l.amount, l.status, 
               l.interest_rate, l.fk_person_id, l.fk_bank_id, 
               p.first_name, p.last_name, p.birthday, p.email, p.phone_number, p.address, p.ssn, p.credit_score,
               b.name as bank_name, b.location as bank_location, b.phone_number as bank_phone_number,
               b.routing_number as bank_routing_number
        FROM loans l
        JOIN people p ON l.fk_person_id = p.person_id
        JOIN banks b ON l.fk_bank_id = b.bank_id
        WHERE 1=1
    """
    params: list[Any] = []
    
    if status:
        query += " AND l.status ILIKE %s"
        params.append(f"%{status}%")
        


    if first_name:
        query += " AND p.first_name ILIKE %s"
        params.append(f"%{first_name}%")

    if last_name:
        query += " AND p.last_name ILIKE %s"
        params.append(f"%{last_name}%")

        
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
        
    valid_sort_fields = {"amount", "interest_rate", "open_date", "term_length", "status", "credit_score"}
    sort_by = kwargs.get("sort_by")
    sort_order = (kwargs.get("sort_order") or "ASC").upper()
    
    if sort_by in valid_sort_fields:
        if sort_order not in {"ASC", "DESC"}:
            sort_order = "ASC"
    
        if sort_by == "credit_score":
            query += f" ORDER BY p.credit_score {sort_order}"
        else:
            query += f" ORDER BY l.{sort_by} {sort_order}"
        
    if kwargs.get("limit") is not None and kwargs.get("offset") is not None:
        query += " LIMIT %s OFFSET %s"
        params.extend([kwargs["limit"], kwargs["offset"]])
        
    return query, tuple(params)


#new query to work with banks join

def get_paginated_loan_with_bank_query(**kwargs: Unpack[GetLoanQueryParams]) -> tuple[str, tuple[Any, ...]]:
    status = kwargs.get("status")
    name = kwargs.get("name")
    bank_id = kwargs.get("bank_id")
    bank_name = kwargs.get("bank_name")  # NEW
    bank_location = kwargs.get("bank_location")  # NEW
    bank_phone = kwargs.get("bank_phone")  # NEW
    min_interest_rate = kwargs.get("min_interest_rate")
    max_interest_rate = kwargs.get("max_interest_rate")
    loan_type = kwargs.get("loan_type")
    sort_order = kwargs.get("sort_order", "ASC").upper()
    
    query = """
        SELECT l.loan_id, l.type, l.open_date, l.term_length, l.amount, l.status, 
               l.interest_rate, l.fk_person_id, l.fk_bank_id, 
               p.first_name, p.last_name, p.birthday, p.email, p.phone_number, p.address, p.ssn, p.credit_score,
               b.name as bank_name, b.location as bank_location, b.phone_number as bank_phone_number,
               b.routing_number as bank_routing_number
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
    if bank_name:
        query += " AND b.name ILIKE %s"
        params.append(f"%{bank_name}%")
    if bank_location:
        query += " AND b.location ILIKE %s"
        params.append(f"%{bank_location}%")
    if bank_phone:
        query += " AND b.phone_number ILIKE %s"
        params.append(f"%{bank_phone}%")
    if min_interest_rate is not None:
        query += " AND l.interest_rate >= %s"
        params.append(min_interest_rate)
    if max_interest_rate is not None:
        query += " AND l.interest_rate <= %s"
        params.append(max_interest_rate)
    if loan_type:
        query += " AND l.type ILIKE %s"
        params.append(f"%{loan_type}%")

    # Sorting
    valid_sort_fields = {"amount", "interest_rate", "open_date", "term_length", "status"}
    sort_by = kwargs.get("sort_by")
    if sort_by in valid_sort_fields:
        query += f" ORDER BY l.{sort_by} {sort_order}"

    if kwargs.get("limit") is not None and kwargs.get("offset") is not None:
        query += " LIMIT %s OFFSET %s"
        params.extend([kwargs["limit"], kwargs["offset"]])

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

