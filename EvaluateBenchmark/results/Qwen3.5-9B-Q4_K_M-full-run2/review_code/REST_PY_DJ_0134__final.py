import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to return.
            - sort_field (str): Field used for ordering.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users"
    params = {
        "include_fields": inputs["included_fields"],
        "sort_field": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    return response.json()