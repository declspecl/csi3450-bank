def get_all_banks():
    """
    Retrieves all banks from the banks table.
    """
    query = "SELECT * FROM banks;"
    return query

def filter_banks_by_name(name_filter):
    """
    Retrieves banks whose names match the search term.
    """
    query = "SELECT * FROM banks WHERE name ILIKE %s"
    params = (f"%{name_filter}%",) # Wrap the filter with % to allow partial matching.
    return query, params

def filter_banks_by_location(location_filter):
    """
    Retrieves banks whose locations match with the search term.
    """
    query = "SELECT * FROM banks WHERE location ILIKE %s;"
    params = (f"%{location_filter}%",)
    return query, params
