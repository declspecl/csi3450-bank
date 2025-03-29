def search_transactions():
    #Retrieves all transactions
    query = "SELECT * FROM transactions"

    return query

def filter_by_person(sender, recipient):
    #Filters transactions based on sender/recipient name
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

def filter_by_account(person_id):
    #Filters transactions given a person's id
    query = "SELECT t.* FROM transactions t JOIN accounts a ON t.account_id = a.account_id WHERE a.person_id = %s"
    params = (f"%{person_id}%",)

    return query, params

def filter_by_status(status):
    #Filters transactions based on the status provided
    query = "SELECT * FROM transactions WHERE status ILIKE %s"
    params = (f"%{status}%",)

    return query, params

def sort_by_amount():
    #Sorts transactions by the amount from highest to lowest
    query = "SELECT  * FROM transactions ORDER BY amount DESC"

    return query

def filter_recent_transactions():
    #Retrieves the most recent transactions and sorts them from most recent to least recent
    query = "SELECT * FROM transactions ORDER BY transaction_date DESC"

    return query

def insert_new_transaction(amount, transaction_date, status, fk_sender_id, fk_recipient_id):
    #Allows a new transaction insertion
    query = "INSERT into transactions (%s, %s, %s, %s, %s)"
    params = (f"%{amount}%", f"%{transaction_date}%", f"%{status}%", f"%{fk_sender_id}%", f"%{fk_recipient_id}%",)

    return query, params