from typing import Optional, TypedDict, Unpack

class GetPartialMatchpersonQueryParams(TypedDict):
    first_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]
    ssn: Optional[str]
    credit_score: Optional[int]
    insert: Optional[bool]
    new_person_id: Optional[int]
    new_first_name: Optional[str]
    new_last_name: Optional[str]
    new_birthday: Optional[str]
    new_email: Optional[str]
    new_phone_number: Optional[str]
    new_address: Optional[str]
    new_ssn: Optional[str]
    new_credit_score: Optional[int]

def get_partial_match_person_query(**kwargs: Unpack[GetPartialMatchpersonQueryParams]) -> tuple[str, tuple]:
    """
    Retrieves a persons information based on the provided filters.
    If not filters are provided, retrieves all person.
    If 'insert' is set to True, inserts a new person with its info.
    """

    # Checks if adding a new person to the database
    insert = kwargs.get("insert", False)

    if insert:
        new_person_id = kwargs.get("new_person_id")
        new_first_name = kwargs.get("new_first_name")
        new_last_name = kwargs.get("new_last_name")
        new_birthday = kwargs.get("new_birthday")
        new_email = kwargs.get("new_email")
        new_phone_number = kwargs.get("new_phone_number")
        new_address = kwargs.get("new_address")
        new_ssn = kwargs.get("new_ssn")
        new_credit_score = kwargs.get("new_credit_score")
        
        if not all([new_person_id, new_first_name, new_last_name, new_birthday, new_email, new_phone_number,new_address, new_ssn, new_credit_score]):
            raise ValueError("All arguments need to be provided for insertion.")
        
        query = """INSERT INTO people (person_id, first_name,last_name, birthday, email, phone_number, address, ssn, credit_score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        params: tuple[int, str, str, str, str, str, str, str, int] = (new_person_id, new_first_name, new_last_name, new_birthday, new_email, new_phone_number, new_address, new_ssn, new_credit_score)
        return query, params

    first_name = kwargs.get("first_name")
    last_name = kwargs.get("last_name")
    address = kwargs.get("address")
    sort_by_credit_score = kwargs.get("credit_score")

    query = "SELECT * FROM people WHERE 1=1"
    params = []

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