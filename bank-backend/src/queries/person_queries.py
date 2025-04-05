from typing import Optional, TypedDict, Unpack

class GetPersonQueryParams(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str]
    address: Optional[str]
    credit_score: Optional[bool]

def get_person_query(**kwargs: Unpack[GetPersonQueryParams]) -> tuple[str, tuple[str, ...]]:
    """
    Retrieves person information based on the provided filters.
    If no filters are provided, retrieves all people.
    """
    first_name = kwargs.get("first_name")
    last_name = kwargs.get("last_name")
    address = kwargs.get("address")
    sort_by_credit_score = kwargs.get("credit_score")

    query = "SELECT * FROM people WHERE 1=1"
    params: list[str] = []

    if first_name:
        query += " AND first_name ILIKE %s"
        params.append(f"%{first_name}%")
    if last_name:
        query += " AND last_name ILIKE %s"
        params.append(f"%{last_name}%")
    if address:
        query += " AND address ILIKE %s"
        params.append(f"%{address}%")
    if sort_by_credit_score:
        query += " ORDER BY credit_score DESC"

    return query, tuple(params)

class InsertPersonParams(TypedDict):
    first_name: str
    last_name: str
    birthday: str
    email: str
    phone_number: str
    address: str
    ssn: str
    credit_score: int

def insert_person_query(params: InsertPersonParams) -> tuple[str, tuple[str, str, str, str, str, str, str, int]]:
    """
    Inserts a new person with the provided information.
    All parameters are required.
    """
    query = """
        INSERT INTO people (first_name, last_name, birthday, email, phone_number, address, ssn, credit_score) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        params["first_name"],
        params["last_name"],
        params["birthday"],
        params["email"],
        params["phone_number"],
        params["address"],
        params["ssn"],
        params["credit_score"]
    )

    return query, values

#Stin - Adding function for pagination will call it in GET request, the other function will be used for inserting a new person in POST request.
def get_paginated_person_query(
    *,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    address: Optional[str] = None,
    credit_score: Optional[int] = None,
    # adding sorting logic
    sort_by: Optional[str] = None,
    sort_order: str = "ASC",
    limit: Optional[int] = None,
    offset: Optional[int] = None
) -> tuple[str, tuple[str | int, ...]]:
    query = "SELECT * FROM people WHERE 1=1"
    params: list[str | int] = []

    if first_name:
        query += " AND first_name ILIKE %s"
        params.append(f"%{first_name}%")
    if last_name:
        query += " AND last_name ILIKE %s"
        params.append(f"%{last_name}%")
    if address:
        query += " AND address ILIKE %s"
        params.append(f"%{address}%")
        
    #allowing for filtering by credit score ie. >= 700    
    if credit_score is not None:
        query += " AND credit_score >= %s"
        params.append(credit_score)
        
    # - Adding sorting logic--------------------------
    valid_sort_fields = {
        "person_id",
        "first_name",
        "last_name",
        "birthday",
        "email",
        "phone_number",
        "address",
        "ssn",
        "credit_score",
    }
    if sort_by in valid_sort_fields:
        sort_order = sort_order.upper()
        if sort_order not in {"ASC", "DESC"}:
            sort_order = "ASC"
        query += f" ORDER BY {sort_by} {sort_order}"


    if limit is not None and offset is not None:
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

    return query, tuple(params)
