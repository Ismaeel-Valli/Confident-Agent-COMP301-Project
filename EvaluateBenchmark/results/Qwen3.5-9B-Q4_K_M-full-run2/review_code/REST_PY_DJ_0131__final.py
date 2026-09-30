import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to return.
            - sort_field (str): Field used for ordering.
    
    Returns:
        dict or None: Decoded JSON response, or None if empty.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/products"
    params = {
        "skip": 0,
        "limit": 1,
        "sort_by": inputs["sort_field"],
        "select": inputs["included_fields"]
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    return response.json() if response.status_code == 200 else None