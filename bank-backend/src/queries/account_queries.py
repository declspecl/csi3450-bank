def search_accounts() -> tuple[str, tuple[()]]:
    """Retrieves all accounts from accounts table"""

    query = "SELECT * FROM accounts"
    params = ()

    return query, params

def filter_by_name(first_name: str, last_name: str) -> tuple[str, tuple[str, str]]:
    """Filters account by a person's name"""

    query = "SELECT * FROM accounts WHERE first_name ILIKE %s AND last_name ILIKE %s"
    params = (f"%{first_name}%", f"%{last_name}%",)

    return query, params
    
def filter_by_account_type(account_type: str) -> tuple[str, tuple[str]]:
    """Retrieves type of account (checking/savings)"""

    query = "SELECT * FROM accounts WHERE account_type ILIKE %s"
    params = (f"%{account_type}%",)

    return query, params
    
def filter_by_status(status: str) -> tuple[str, tuple[str]]:
    """Filters accounts based on the status provided"""

    query = "SELECT * FROM accounts WHERE status ILIKE %s"
    params= (f"%{status}%",)

    return query, params
    
def sort_by_balance() -> tuple[str, tuple[()]]:
    """Sorts accounts based on the account balance from highest to lowest"""

    query = "SELECT * FROM accounts ORDER BY balance DESC"
    params = ()

    return query, params
    
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