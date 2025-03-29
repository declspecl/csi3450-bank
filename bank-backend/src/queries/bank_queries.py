from typing import Optional, TypedDict, Unpack

class GetPartialMatchBanksQueryParams(TypedDict):
    name: Optional[str]
    location: Optional[str]
    insert: Optional[bool]
    new_bankid: Optional[int]
    new_name: Optional[str]
    new_location: Optional[str]
    new_routing_number: Optional[str]
    new_phone_number: Optional[str]

def get_partial_match_banks_query(**kwargs: Unpack[GetPartialMatchBanksQueryParams]) -> tuple[str, tuple[str, str]]:
    """
    Retrieves banks based on the provided filters.
    If no filters are provided, retrieves all banks.
    If 'insert' is set to True, inserts a new bank with a new name & location
    """

    # Will check if inserting a new bank
    insert = kwargs.get("insert", False)

    if insert:
        new_id = kwargs.get("new_bankid")
        new_name = kwargs.get("new_name")
        new_location = kwargs.get("new_location")
        new_routing_number = kwargs.get("new_routing_number")
        new_phone_number = kwargs.get("new_phone_number")

        if not all([new_id, new_name, new_location, new_routing_number, new_phone_number]):
            raise ValueError("All arguments need to be provided for insertion.")

        query = "INSERT INTO banks (bank_id, name, location, routing_number, phone_number) VALUES (%s, %s, %s, %s, %s)"
        params: tuple[int, str, str, str, str] = (new_id, new_name, new_location, new_routing_number, new_phone_number)
        return query, params


    name = kwargs.get("name")
    location = kwargs.get("location")

    query = "SELECT * FROM banks WHERE name ILIKE %s AND location ILIKE %s"
    params: tuple[str, str] = (
        "%{}%".format(name if name else ""),
        "%{}%".format(location if location else "")
    )

    return query, params