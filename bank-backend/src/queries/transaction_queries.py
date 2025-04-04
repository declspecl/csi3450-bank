from typing import Optional, TypedDict, Unpack

class GetPartialMatchTransactionQueryParams(TypedDict):
    status: Optional[str]
    sort_by_amount: Optional[bool]
    recent: Optional[bool]
    insert: Optional[bool]
    new_amount: Optional[float]
    new_transaction_date: Optional[str]
    new_status: Optional[str]
    new_fk_sender_id: Optional[int]
    new_fk_recipient_id: Optional[int]

def get_partial_match_transaction_query(**kwargs: Unpack[GetPartialMatchTransactionQueryParams]) -> tuple[str, tuple]:
    """
    Retrieves transaction information based on the provided filters.
    If no filters are provided, retrieves all transactions.
    If 'insert' is set to True, inserts a new transaction with its info.
    """
    insert = kwargs.get("insert", False)

    if insert:
        new_amount = kwargs.get("new_amount")
        new_transaction_date = kwargs.get("new_transaction_date")
        new_status = kwargs.get("new_status")
        new_fk_sender_id = kwargs.get("new_fk_sender_id")
        new_fk_recipient_id = kwargs.get("new_fk_recipient_id")

        if not all([new_amount, new_transaction_date, new_status, new_fk_sender_id, new_fk_recipient_id]):
            raise ValueError("All arguments need to be provided for insertion.")

        query = """
            INSERT INTO transactions (amount, transaction_date, status, fk_sender_id, fk_recipient_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (new_amount, new_transaction_date, new_status, new_fk_sender_id, new_fk_recipient_id)
        return query, params

    status = kwargs.get("status")
    sort_by_amount = kwargs.get("sort_by_amount", False)
    recent = kwargs.get("recent", False)

    query = "SELECT * FROM transactions WHERE 1=1"
    params = []

    if status:
        query += " AND status ILIKE %s"
        params.append(f"%{status}%")
    if sort_by_amount:
        query += " ORDER BY amount DESC"
    if recent:
        query += " ORDER BY transaction_date DESC"

    return query, tuple(params)
