import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON, sorted by sort_field in sort_direction.
    
    Args:
        inputs (dict): Must contain 'sort_field' and 'sort_direction'.
        
    Returns:
        list or None: Decoded JSON response (list of users), or None if empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users"
    
    # Validate inputs
    sort_field = inputs.get("sort_field")
    sort_direction = inputs.get("sort_direction")
    
    if sort_field is None or sort_direction is None:
        raise ValueError("Missing required input fields: 'sort_field' and 'sort_direction'")
    
    params = {
        "sort": sort_field,
        "order": sort_direction
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty list, otherwise return the list of users
    if not data.get("users"):
        return None
    
    return data["users"]