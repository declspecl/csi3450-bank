from typing import Optional, TypedDict, Unpack

class GetAccountQueryParams(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str] 
    account_type: Optional[str]
    status: Optional[str]
    sort_by_balance: Optional[bool]
    page: Optional[int]
    page_size: Optional[int]

def get_account_query(**kwargs: Unpack[GetAccountQueryParams]) -> tuple[str, tuple[str, ...]]:
    """
    Retrieves account information based on the provided filters.
    If no filters are provided, retrieves all accounts.
    """
    first_name = kwargs.get("first_name")
    last_name = kwargs.get("last_name")
    account_type = kwargs.get("account_type") 
    status = kwargs.get("status")
    sort_by_balance = kwargs.get("sort_by_balance", False)
    page = kwargs.get("page", 1)
    page_size = kwargs.get("page_size", 15)

    query = "SELECT * FROM accounts WHERE 1=1"
    params: list[str] = []

    if first_name:
        query += " AND first_name ILIKE %s"
        params.append(f"%{first_name}%")
    if last_name:
        query += " AND last_name ILIKE %s"
        params.append(f"%{last_name}%")
    if account_type:
        query += " AND account_type ILIKE %s"
        params.append(f"%{account_type}%")
    if status:
        query += " AND status ILIKE %s"
        params.append(f"%{status}%")
    if sort_by_balance:
        query += " ORDER BY balance DESC"
    if page and page_size:
        offset = (page - 1) * page_size
        query += f" LIMIT {page_size} OFFSET {offset}"

    return query, tuple(params)

class InsertAccountParams(TypedDict):
    account_number: str
    routing_number: str
    account_type: str
    balance: float
    status: str
    fk_person_id: int
    fk_bank_id: int

def get_paginated_account_query(
    fk_person_id: Optional[int] = None,
    account_type: Optional[str] = None,
    status: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "ASC",
    limit: int = 15,
    offset: int = 0
) -> tuple[str, tuple[str | int, ...]]:
    """
    Returns a SQL query for fetching accounts with optional filters and sorting.
    """
    query = """
        SELECT a.account_number, a.routing_number, a.account_type, a.balance, a.status,
               a.fk_person_id, a.fk_bank_id, b.name AS bank_name
        FROM accounts a
        JOIN people p ON a.fk_person_id = p.person_id
        JOIN banks b ON a.fk_bank_id = b.bank_id
        WHERE 1=1
    """
    params: list[int | str] = []

    if fk_person_id:
        query += " AND a.fk_person_id = %s"
        params.append(fk_person_id)

    if account_type:
        query += " AND a.account_type ILIKE %s"
        params.append(f"%{account_type}%")

    if status:
        query += " AND a.status ILIKE %s"
        params.append(f"%{status}%")


    valid_sort_fields = {
        "account_number", 
        "routing_number", 
        "account_type",
        "balance", 
        "status"
    }
    if sort_by in valid_sort_fields:
        sort_order = sort_order.upper()
        if sort_order not in ["ASC", "DESC"]:
            sort_order = "ASC"
        query += f" ORDER BY {sort_by} {sort_order}"

    if limit and offset:
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])


    return query, tuple(params)

def insert_account_query(params: InsertAccountParams) -> tuple[str, tuple[str, str, str, float, str, int, int]]:
    """
    Inserts a new account with the provided information.
    All parameters are required.
    """
    query = """
        INSERT INTO accounts (account_number, routing_number, account_type, balance, status, fk_person_id, fk_bank_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        params["account_number"],
        params["routing_number"], 
        params["account_type"],
        params["balance"],
        params["status"],
        params["fk_person_id"],
        params["fk_bank_id"]
    )

    return query, values
