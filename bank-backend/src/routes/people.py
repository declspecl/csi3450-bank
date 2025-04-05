from server import app, conn
from flask import request, jsonify, Response
from queries.person_queries import get_paginated_person_query, insert_person_query

class Person:
    def __init__(self, person_id: int, first_name: str, last_name: str, birthday: str, 
                 email: str, phone_number: str, address: str, ssn: str, credit_score: int):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.ssn = ssn
        self.credit_score = credit_score
        
    def __repr__(self) -> str:
        return f"Person({self.person_id}, {self.first_name}, {self.last_name})"
        
    def to_json(self) -> dict[str, str | int]:
        return {
            "person_id": self.person_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthday": self.birthday,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "ssn": self.ssn, 
            "credit_score": self.credit_score
        }
    

# POST and GET methods for person route
@app.route("/people", methods=["GET"])
def get_people() -> tuple[Response, int]:
    """
    Handles GET requests to retrieve a persons information based on provided paramaters.
    """
    cursor = conn.cursor()

    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    address = request.args.get("address")
    
    #Stin adding type = int to credit_score to ensure it is an integer for filtering
    sort_by_credit_score = request.args.get("credit_score", type = int)
    
    #Stin - Adding sorting--------------------------
    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order", default="ASC")
    #Stin - Adding pagination--------------------------
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=20, type=int)
    limit = page_size
    offset = (page - 1) * page_size
    
    query, params = get_paginated_person_query(
    first_name=first_name,
    last_name=last_name,
    address=address,
    credit_score=sort_by_credit_score,
    sort_by=sort_by,
    sort_order=sort_order,
    limit=limit,
    offset=offset
)#-----------------------------------------------

#commenting out old code as the new code handles pagination and queries
#keeping it for reference
    # print(f"Got request to /person with params: first_name={first_name}, last_name={last_name}, address={address}, credit_score={sort_by_credit_score}")

    # query, params = get_partial_match_person_query(
        # first_name=first_name,
        # last_name=last_name,
        # address=address,
        # credit_score=sort_by_credit_score
    # )

    try:
        cursor.execute(query, params)
        person_rows = cursor.fetchall()
        conn.commit()
        
        #Stin - adding code to get total number of people----------------
        cursor2 = conn.cursor()
        cursor2.execute("SELECT COUNT(*) FROM people")
        count_row = cursor2.fetchone()
        assert count_row is not None
        total_count = count_row[0]
        cursor2.close()
        #------------------------------
    except Exception as e:
        print(f"Error executing query: {e}")
        conn.rollback()
        return jsonify([]), 500
    finally:
        cursor.close()
    people: list[object] = []
    for row in person_rows:
        people.append({
            "person_id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "birthday": str(row[3]),
            "email": row[4],
            "phone_number": row[5],
            "address": row[6],
            "ssn": row[7],
            "credit_score": row[8]
        })
    #Stin- updating return statement to include total number of people
    return jsonify({
        "people": people,
        "total_count": total_count
        }), 200

@app.route("/people", methods=["POST"])
def create_new_person() -> tuple[Response, int]:
    """
    Handles POST requests to insert a new person.
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    #Stin - removing person_id from params as it is not needed for insertion
    #new_person_id = data.get("person_id")
    new_first_name = data.get("first_name")
    new_last_name = data.get("last_name")
    new_birthday = data.get("birthday")
    new_email = data.get("email")
    new_phone_number = data.get("phone_number")
    new_address = data.get("address")
    new_ssn = data.get("ssn")
    new_credit_score = data.get("credit_score")

    if not all([new_first_name, new_last_name, new_birthday, new_email, new_phone_number, new_address, new_ssn, new_credit_score]):
        return jsonify({"error": "All fields are required: first_name, last_name, birthday, email, phone_number, address, ssn, credit_score"}), 400

    query, params = insert_person_query(
        first_name=new_first_name,
        last_name=new_last_name,
        birthday=new_birthday,
        email=new_email,
        phone_number=new_phone_number,
        address=new_address,
        ssn=new_ssn,
        credit_score=new_credit_score
    )

    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return jsonify({"message": "Person inserted successfully!"}), 201
    except Exception as e:
        conn.rollback()
        print(f"Error inserting person: {e}")
        return jsonify({"error": "Failed to insert person"}), 500
    finally:
        cursor.close()