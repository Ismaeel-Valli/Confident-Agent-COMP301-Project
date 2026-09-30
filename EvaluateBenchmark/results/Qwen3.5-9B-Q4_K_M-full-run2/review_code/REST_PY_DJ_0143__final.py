import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON, sorted by sort_field in sort_direction.
    
    Args:
        inputs (dict): Must contain 'sort_field' and 'sort_direction'.
        
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users"
    
    params = {
        "sort": inputs["sort_field"],
        "order": inputs["sort_direction"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    return response.json()