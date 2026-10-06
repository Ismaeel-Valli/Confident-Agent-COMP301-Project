import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON with specified fields and sorting.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to include
            - sort_field (str): Field to sort by
    
    Returns:
        dict or None: Decoded JSON response, or None if empty
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/users"
    
    # Parse included fields
    included_fields_list = [f.strip() for f in inputs["included_fields"].split(",")]
    
    # Build query parameters
    params = {
        "include_fields": ",".join(included_fields_list),
        "sort_by": inputs["sort_field"],
        "limit": 1,  # One page of users
        "skip": 0
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    # Return None for empty response
    if not data.get("users") or len(data["users"]) == 0:
        return None
    
    return data