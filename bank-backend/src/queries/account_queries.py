from typing import Optional, TypedDict, Unpack

#Stin okay I am going to create a function to combine all the functionality into one function
#also i need to add ability of pagination
#so I might comment out this code

#Stin Code------------------------------------------------------------------------
def get_paginated_account_query(
    fk_person_id=None,
    account_type=None,
    status=None,
    # sorting logic
    sort_by=None,
    sort_order="ASC",
    limit=15,
    offset=0
) -> tuple[str, tuple]:
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
    params = []

    if fk_person_id:
        query += " AND a.fk_person_id = %s"
        params.append(fk_person_id)

    if account_type:
        query += " AND a.account_type ILIKE %s"
        params.append(f"%{account_type}%")

    if status:
        query += " AND a.status ILIKE %s"
        params.append(f"%{status}%")


    #adding sorting logic to the query
    #same as person_queries.py
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

    if limit is not None and offset is not None:
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])


    return query, tuple(params)

#-----------------------------------------------------------

#needed this one hehe thank you bernard
def insert_new_account(
    account_number: str,
    routing_number: str,
    account_type: str,
    balance: float,
    status: str,
    fk_person_id: int,
    fk_bank_id: int
) -> tuple[str, tuple[str, str, str, float, str, int, int]]:
    """Allows a new bank account insertion"""
    query = "INSERT INTO accounts (account_number, routing_number, account_type, balance, status, fk_person_id, fk_bank_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    params = (account_number, routing_number, account_type, balance, status, fk_person_id, fk_bank_id)

    return query, params


#Blocked out code for now as I am not sure if I need it yet
# put a "\" in front of triple quotes to block out the code
"""
def search_accounts() -> tuple[str, tuple[()]]:
    \"\"\"Retrieves all accounts from accounts table\"\"\"

    query = "SELECT * FROM accounts"
    params = ()

    return query, params

def filter_by_name(first_name: str, last_name: str) -> tuple[str, tuple[str, str]]:
    \"\"\"Filters account by a person's name\"\"\"

    query = "SELECT * FROM accounts WHERE first_name ILIKE %s AND last_name ILIKE %s"
    params = (f"%{first_name}%", f"%{last_name}%",)

    return query, params
    
def filter_by_account_type(account_type: str) -> tuple[str, tuple[str]]:
    \"\"\"Retrieves type of account (checking/savings)\"\"\"

    query = "SELECT * FROM accounts WHERE account_type ILIKE %s"
    params = (f"%{account_type}%",)

    return query, params
    
def filter_by_status(status: str) -> tuple[str, tuple[str]]:
    \"\"\"Filters accounts based on the status provided\"\"\"

    query = "SELECT * FROM accounts WHERE status ILIKE %s"
    params= (f"%{status}%",)

    return query, params
    
def sort_by_balance() -> tuple[str, tuple[()]]:
    \"\"\"Sorts accounts based on the account balance from highest to lowest\"\"\"

    query = "SELECT * FROM accounts ORDER BY balance DESC"
    params = ()

    return query, params
    

"""

class GetPartialMatchAccountQueryParams(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str]
    account_type: Optional[str]
    status: Optional[str]
    sort_by_balance: Optional[bool]
    insert: Optional[bool]
    new_account_number: Optional[str]
    new_routing_number: Optional[str]
    new_account_type: Optional[str]
    new_balance: Optional[float]
    new_status: Optional[str]
    new_fk_person_id: Optional[int]
    new_fk_bank_id: Optional[int]

def get_partial_match_account_query(**kwargs: Unpack[GetPartialMatchAccountQueryParams]) -> tuple[str, tuple]:
    """
    Retrieves account information based on the provided filters.
    If no filters are provided, retrieves all accounts.
    If 'insert' is set to True, inserts a new account with its info.
    """
    insert = kwargs.get("insert", False)

    if insert:
        new_account_number = kwargs.get("new_account_number")
        new_routing_number = kwargs.get("new_routing_number")
        new_account_type = kwargs.get("new_account_type")
        new_balance = kwargs.get("new_balance")
        new_status = kwargs.get("new_status")
        new_fk_person_id = kwargs.get("new_fk_person_id")
        new_fk_bank_id = kwargs.get("new_fk_bank_id")

        if not all([new_account_number, new_routing_number, new_account_type, new_balance, new_status, new_fk_person_id, new_fk_bank_id]):
            raise ValueError("All arguments need to be provided for insertion.")

        query = """
            INSERT INTO accounts (account_number, routing_number, account_type, balance, status, fk_person_id, fk_bank_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (new_account_number, new_routing_number, new_account_type, new_balance, new_status, new_fk_person_id, new_fk_bank_id)
        return query, params

    first_name = kwargs.get("first_name")
    last_name = kwargs.get("last_name")
    account_type = kwargs.get("account_type")
    status = kwargs.get("status")
    sort_by_balance = kwargs.get("sort_by_balance", False)

    query = "SELECT * FROM accounts WHERE 1=1"
    params = []

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

    return query, tuple(params)
