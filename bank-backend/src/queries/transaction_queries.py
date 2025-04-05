from typing import Optional, TypedDict, Unpack

class GetTransactionQueryParams(TypedDict):
    status: Optional[str]
    sort_by_amount: Optional[bool]
    recent: Optional[bool]

def get_transaction_query(**kwargs: Unpack[GetTransactionQueryParams]) -> tuple[str, tuple[str | float | int, ...]]:
    """
    Retrieves transaction information based on the provided filters.
    If no filters are provided, retrieves all transactions.
    """
    status = kwargs.get("status")
    sort_by_amount = kwargs.get("sort_by_amount", False)
    recent = kwargs.get("recent", False)

    query = "SELECT * FROM transactions WHERE 1=1"
    params: list[str | float | int] = []

    if status:
        query += " AND status ILIKE %s"
        params.append(f"%{status}%")
    if sort_by_amount:
        query += " ORDER BY amount DESC"
    if recent:
        query += " ORDER BY transaction_date DESC"

    return query, tuple(params)

class InsertTransactionParams(TypedDict):
    amount: float
    transaction_date: str
    status: str
    fk_sender_id: int
    fk_recipient_id: int

def insert_transaction_query(params: InsertTransactionParams) -> tuple[str, tuple[float, str, str, int, int]]:
    """
    Inserts a new transaction with the provided information.
    All parameters are required.
    """
    query = """
        INSERT INTO transactions (amount, transaction_date, status, fk_sender_id, fk_recipient_id)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        params["amount"],
        params["transaction_date"],
        params["status"],
        params["fk_sender_id"],
        params["fk_recipient_id"]
    )

    return query, values
