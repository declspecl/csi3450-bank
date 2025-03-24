from typing import Optional, TypedDict, Unpack

class GetPartialMatchBanksQueryParams(TypedDict):
    name: Optional[str]
    location: Optional[str]

def get_partial_match_banks_query(**kwargs: Unpack[GetPartialMatchBanksQueryParams]) -> tuple[str, tuple[str, str]]:
    """
    Retrieves banks based on the provided filters.
    If no filters are provided, retrieves all banks.
    """

    name = kwargs.get("name")
    location = kwargs.get("location")

    query = "SELECT * FROM banks WHERE name ILIKE %s AND location ILIKE %s"
    params: tuple[str, str] = (
        "%{}%".format(name if name else ""),
        "%{}".format(location if location else "")
    )

    return query, params