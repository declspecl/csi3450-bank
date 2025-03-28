def search_accounts():
    #Retrieves all accounts from accounts table
    query = "SELECT * FROM accounts"

    return query

def filter_by_name(first_name, last_name):
    #Filters account by a person's name
    query = "SELECT * FROM accounts WHERE first_name ILIKE %s AND last_name ILIKE %s"
    params = (f"%{first_name}%", f"%{last_name}%",)

    return query, params
    
def filter_by_account_type(account_type):
    #Retrieves type of account (checking/savings)
    query = "SELECT * FROM accounts WHERE account_type ILIKE %s"
    params = (f"%{account_type}%",)

    return query, params
    
def filter_by_status(status):
    #Filters accounts based on the status provided
    query = "SELECT * FROM accounts WHERE status ILIKE %s"
    params= (f"%{status}%",)

    return query, params
    
def sort_by_balance():
    #Sorts accounts based on the account balance from highest to lowest
    query = "SELECT * FROM accounts ORDER BY balance DESC"

    return query
    
def insert_new_account(account_id, account_number, routing_number, account_type, balance, status, fk_person_id, fk_bank_id):
    #Allows a new bank account insertion
    query = "INSERT INTO accounts (%s, %s, %s, %s, %s, %s, %s, %s)"
    params = (f"%{account_id}%", f"%{account_number}%", f"%{routing_number}%", f"%{account_type}%", f"%{balance}%", f"%{status}%", f"%{fk_person_id}%", f"%{fk_bank_id}%",)

    return query, params