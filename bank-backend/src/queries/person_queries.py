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

def insert_person_query(**params: Unpack[InsertPersonParams]) -> tuple[str, tuple[str, str, str, str, str, str, str, int]]:
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

class GetPaginatedPersonQueryParams(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str]
    address: Optional[str]
    credit_score: Optional[int]
    sort_by: Optional[str]
    sort_order: str
    limit: Optional[int]
    offset: Optional[int]

def get_paginated_person_query(**kwargs: Unpack[GetPaginatedPersonQueryParams]) -> tuple[str, tuple[str | int, ...]]:
    query = "SELECT * FROM people WHERE 1=1"
    params: list[str | int] = []

    first_name = kwargs.get("first_name")
    last_name = kwargs.get("last_name")
    address = kwargs.get("address")
    credit_score = kwargs.get("credit_score")
    if first_name:
        query += " AND first_name ILIKE %s"
        params.append(f"%{first_name}%")
    if last_name:
        query += " AND last_name ILIKE %s"
        params.append(f"%{last_name}%")
    if address:
        query += " AND address ILIKE %s"
        params.append(f"%{address}%")
        
    credit_score = kwargs.get("credit_score")
    if credit_score is not None:
        query += " AND credit_score >= %s"
        params.append(credit_score)
        
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

    sort_by = kwargs.get("sort_by")
    if sort_by in valid_sort_fields:
        sort_order = kwargs.get("sort_order").upper()
        if sort_order not in {"ASC", "DESC"}:
            sort_order = "ASC"

        query += f" ORDER BY {sort_by} {sort_order}"

    limit = kwargs.get("limit")
    offset = kwargs.get("offset")
    if limit is not None and offset is not None:
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

    return query, tuple(params)
