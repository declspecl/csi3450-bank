from typing import TypedDict, Unpack

class GetPartialMatchBanksQueryParams(TypedDict):
    name: str
    location: str

def get_partial_match_banks_query(**kwargs: Unpack[GetPartialMatchBanksQueryParams]) -> tuple[str, tuple[str, str]]:
    """
    Retrieves banks based on the provided filters.
    If no filters are provided, retrieves all banks.
    """

    kwargs.setdefault("name", "")
    kwargs.setdefault("location", "")

    query = "SELECT * FROM banks WHERE name ILIKE %s AND location ILIKE %s"
    params = (kwargs.get("name"), kwargs.get("location"))

    return query, params