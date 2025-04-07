from typing import Optional, TypedDict, Unpack

#UPDATING FOR PAGINATION AND SORTING

class GetTransactionQueryParams(TypedDict):
    status: Optional[str]
    sort_by_amount: Optional[bool]
    recent: Optional[bool]
    sort_order: Optional[str]
    limit: Optional[int]
    offset: Optional[int]

def get_paginated_transaction_query(**kwargs: Unpack[GetTransactionQueryParams]) -> tuple[str, tuple[str | int]]:

    query = "SELECT * FROM transactions WHERE 1=1"
    params: list[str | int] = []

    if kwargs.get("status"):
        query += " AND status ILIKE %s"
        params.append(f"%{kwargs['status']}%")

    valid_sort_fields = {"amount", "transaction_date", "transaction_id"}
    sort_by = kwargs.get("sort_by")
    sort_order = kwargs.get("sort_order", "ASC").upper()
    if sort_by in valid_sort_fields:
        if sort_order not in {"ASC", "DESC"}:
            sort_order = "ASC"
        query += f" ORDER BY {sort_by} {sort_order}"

    query += " LIMIT %s OFFSET %s"
    params.extend([kwargs["limit"], kwargs["offset"]])

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
