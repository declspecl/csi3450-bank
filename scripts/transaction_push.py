def add_transaction(conn, cursor, amount, transaction_date, status, sender_id, recipient_id):
    
    try:
        # Ensure sender and recipient are different
        if sender_id == recipient_id:
            print("[!] Error: Sender and recipient cannot be the same.")
            return
        
        query = """
            INSERT INTO transactions (amount, transaction_date, status, fk_sender_id, fk_recipient_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (amount, transaction_date, status, sender_id, recipient_id))
        conn.commit()
        print("[+] Transaction added successfully!")
    except Exception as e:
        print("[!] Error adding transaction:", e)

""" To add to Main """
if input("[?] Do you want to add a transaction? (Y/n) ").strip().lower() == "y":
    amount = float(input("Enter amount: "))
    transaction_date = input("Enter transaction date (YYYY-MM-DD): ").strip()
    status = input("Enter transaction status: ").strip()
    sender_id = int(input("Enter sender account ID: "))
    recipient_id = int(input("Enter recipient account ID: "))
    
    add_transaction(conn, cursor, amount, transaction_date, status, sender_id, recipient_id)
