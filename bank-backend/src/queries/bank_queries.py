from typing import Optional, TypedDict, Unpack


class GetBankQueryParams(TypedDict):
    name: Optional[str]
    location: Optional[str]
    limit: Optional[int]
    offset: Optional[int]
    sort_by: Optional[str]  # Added for sorting
    sort_order: Optional[str]  # Added for sorting
def get_bank_query(**kwargs: Unpack[GetBankQueryParams]) -> tuple[str, tuple[str | int, ...]]:
    query = "SELECT * FROM banks WHERE 1=1"
    params: list[str | int] = []

    if kwargs.get("name"):
        query += " AND name ILIKE %s"
        params.append(f"%{kwargs['name']}%")

    if kwargs.get("location"):
        query += " AND location ILIKE %s"
        params.append(f"%{kwargs['location']}%")

    # Sorting Logic (with safe defaults)
    sort_by = kwargs.get("sort_by", "name")
    sort_order = kwargs.get("sort_order", "asc")

    # Prevent SQL Injection by validating sort_by and sort_order
    valid_sort_by = {"name", "location"}
    sort_by = sort_by if sort_by in valid_sort_by else "name"

    sort_order = "DESC" if sort_order.lower() == "desc" else "ASC"

    query += f" ORDER BY {sort_by} {sort_order}"

    # Pagination logic
    if kwargs.get("limit") is not None and kwargs.get("offset") is not None:
        query += " LIMIT %s OFFSET %s"
        params.extend([kwargs["limit"], kwargs["offset"]])

    return query, tuple(params)

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
