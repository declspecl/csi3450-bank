def search_transactions() -> tuple[str, tuple[()]]:
    """Retrieves all transactions"""

    query = "SELECT * FROM transactions"
    params = ()

    return query, params

def filter_by_person(sender: str, recipient: str) -> tuple[str, tuple[str, str]]:
    """Filters transactions based on sender/recipient name"""

    query = """
        SELECT t.* 
        FROM transactions t
        JOIN accounts sender_acc ON t.fk_sender_id = sender_acc.account_id
        JOIN people sender_person ON sender_acc.fk_person_id = sender_person.person_id
        JOIN accounts recipient_acc ON t.fk_recipient_id = recipient_acc.account_id
        JOIN people recipient_person ON recipient_acc.fk_person_id = recipient_person.person_id
        WHERE CONCAT(sender_person.first_name, ' ', sender_person.last_name) ILIKE %s
        AND CONCAT(recipient_person.first_name, ' ', recipient_person.last_name) ILIKE %s
    """
    params = (f"%{sender}%", f"%{recipient}%",)

    return query, params

def filter_by_account(person_id: int) -> tuple[str, tuple[str]]:
    """Filters transactions given a person's id"""

    query = "SELECT t.* FROM transactions t JOIN accounts a ON t.account_id = a.account_id WHERE a.person_id = %s"
    params = (f"%{person_id}%",)

    return query, params

def filter_by_status(status: str) -> tuple[str, tuple[str]]:
    """Filters transactions based on the status provided"""

    query = "SELECT * FROM transactions WHERE status ILIKE %s"
    params = (f"%{status}%",)

    return query, params

def sort_by_amount() -> tuple[str, tuple[()]]:
    """Sorts transactions by the amount from highest to lowest"""

    query = "SELECT  * FROM transactions ORDER BY amount DESC"
    params = ()

    return query, params

def filter_recent_transactions() -> tuple[str, tuple[()]]:
    """Retrieves the most recent transactions and sorts them from most recent to least recent"""

    query = "SELECT * FROM transactions ORDER BY transaction_date DESC"
    params = ()

    return query, params

def insert_new_transaction(
    amount: float,
    transaction_date: str,
    status: str,
    fk_sender_id: int,
    fk_recipient_id: int
) -> tuple[str, tuple[float, str, str, int, int]]:
    """Allows a new transaction insertion"""

    query = "INSERT into transactions (%s, %s, %s, %s, %s)"
    params = (amount, transaction_date, status, fk_sender_id, fk_recipient_id)

    return query, params