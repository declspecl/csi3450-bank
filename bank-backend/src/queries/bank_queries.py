from typing import Optional, TypedDict, Unpack

class GetBankQueryParams(TypedDict):
    name: Optional[str]
    location: Optional[str]

def get_bank_query(**kwargs: Unpack[GetBankQueryParams]) -> tuple[str, tuple[str, str]]:
    """
    Retrieves banks based on the provided filters.
    If no filters are provided, retrieves all banks.
    """

    name = kwargs.get("name")
    location = kwargs.get("location")

    query = "SELECT * FROM banks WHERE name ILIKE %s AND location ILIKE %s"
    params: tuple[str, str] = (
        "%{}%".format(name if name else ""),
        "%{}%".format(location if location else "")
    )

    return query, params

class InsertBankQueryParams(TypedDict):
    new_name: Optional[str]
    new_location: Optional[str]
    new_routing_number: Optional[str]
    new_phone_number: Optional[str]

def insert_bank_query(**kwargs: Unpack[InsertBankQueryParams]) -> tuple[str, tuple[str, str, str, str]]:
    """
    Inserts a new bank into the database.
    """

    new_name = kwargs.get("new_name")
    new_location = kwargs.get("new_location")
    new_routing_number = kwargs.get("new_routing_number")
    new_phone_number = kwargs.get("new_phone_number")

    if not all([new_name, new_location, new_routing_number, new_phone_number]):
        raise ValueError("All arguments need to be provided for insertion.")

    assert new_name is not None
    assert new_location is not None
    assert new_routing_number is not None
    assert new_phone_number is not None

    query = "INSERT INTO banks (name, location, routing_number, phone_number) VALUES (%s, %s, %s, %s)"
    params: tuple[str, str, str, str] = (
        new_name,
        new_location,
        new_routing_number,
        new_phone_number
    )
    return query, params
