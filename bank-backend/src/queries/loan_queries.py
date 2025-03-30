def search_loans():
    # Retrieves all loans from the loans table
    query = "SELECT * FROM loans"
    return query

def filter_by_status(status):
    # Filters loans based on their status
    query = "SELECT * FROM loans WHERE status ILIKE %s"
    params = (f"%{status}%",)
    return query, params

def sort_by_loan_amount(order="DESC"):
    # Sorts loans by loan amount defualt should be set highest to loswest 
    if order.upper() not in ["ASC", "DESC"]:
        raise ValueError("Invalid order. Use 'ASC' or 'DESC'.")
    query = f"SELECT * FROM loans ORDER BY loan_amount {order}"
    return query

def filter_by_customer_name(first_name, last_name):
    # Filters loans by a customer's name 
    query = "SELECT * FROM loans WHERE first_name ILIKE %s AND last_name ILIKE %s"
    params = (f"%{first_name}%", f"%{last_name}%")
    return query, params

def filter_by_bank(bank_name):
    # Filters loans by the bank name
    query = "SELECT * FROM loans WHERE bank_name ILIKE %s"
    params = (f"%{bank_name}%",)
    return query, params

def filter_by_interest_rate(min_rate, max_rate):
    # Filters loans based on an interest rate 
    query = "SELECT * FROM loans WHERE interest_rate BETWEEN %s AND %s"
    params = (min_rate, max_rate)
    return query, params

def filter_by_loan_type(loan_type):
    # Filters loans by the type of loan
    query = "SELECT * FROM loans WHERE loan_type ILIKE %s"
    params = (f"%{loan_type}%",)
    return query, params

def insert_new_loan(loan_id, customer_id, loan_amount, interest_rate, loan_date, status, loan_type, bank_name):
    # Inserts a new loan into the loans table
    query = """
        INSERT INTO loans (loan_id, customer_id, loan_amount, interest_rate, loan_date, status, loan_type, bank_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        loan_id,
        customer_id,
        loan_amount,
        interest_rate,
        loan_date,
        status,
        loan_type,
        bank_name
    )
    return query, params

def update_loan_status(loan_id, status):
    # Updates the status of a loan by loan ID
    query = "UPDATE loans SET status = %s WHERE loan_id = %s"
    params = (status, loan_id)
    return query, params

def delete_loan(loan_id):
    # Deletes a loan by loan ID
    query = "DELETE FROM loans WHERE loan_id = %s"
    params = (loan_id,)
    
    return query, params
