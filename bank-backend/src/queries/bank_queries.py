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
    name: Optional[str]
    location: Optional[str]
    routing_number: Optional[str]
    phone_number: Optional[str]

def insert_bank_query(**kwargs: Unpack[InsertBankQueryParams]) -> tuple[str, tuple[str, str, str, str]]:
    """
    Inserts a new bank into the database.
    """

    name = kwargs.get("name")
    location = kwargs.get("location")
    routing_number = kwargs.get("routing_number")
    phone_number = kwargs.get("phone_number")

    if not all([name, location, routing_number, phone_number]):
        raise ValueError("All arguments need to be provided for insertion.")

    assert name is not None
    assert location is not None
    assert routing_number is not None
    assert phone_number is not None

    query = "INSERT INTO banks (name, location, routing_number, phone_number) VALUES (%s, %s, %s, %s)"
    params: tuple[str, str, str, str] = (
        name,
        location,
        routing_number,
        phone_number
    )

    return query, params
