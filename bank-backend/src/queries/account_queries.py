from typing import Optional, TypedDict, Unpack

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