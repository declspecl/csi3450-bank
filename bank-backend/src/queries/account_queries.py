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