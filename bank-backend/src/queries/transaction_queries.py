def search_transactions():
    #Retrieves all transactions
    query = "SELECT * FROM transactions"

    return query

def filter_by_person(sender, recipient):
    #Filters transactions based on sender/recipient name
    query = "SELECT * FROM transactions WHERE sender ILIKE %s AND recipient ILIKE %s"

    return query

def filter_by_account(person_id):
    #Filters transactions given a person's id
    query = "SELECT * FROM transactions WHERE person_id ILIKE %s"
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

def insert_new_transaction(transaction_id, amount, transaction_date, status, fk_sender_id, fk_recipient_id):
    #Allows a new transaction insertion
    query = "INSERT into transactions (%s, %s, %s, %s, %s, %s)"
    params = (f"%{transaction_id}%", f"%{amount}%", f"%{transaction_date}%", f"%{status}%", f"%{fk_sender_id}%", f"%{fk_recipient_id}%",)

    return query, params