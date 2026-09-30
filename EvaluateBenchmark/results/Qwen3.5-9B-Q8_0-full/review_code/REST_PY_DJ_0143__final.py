import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON, sorted by sort_field in sort_direction.
    
    Args:
        inputs (dict): Must contain 'sort_field' and 'sort_direction'.
        
    Returns:
        list or None: Decoded JSON response as a list, or None if empty.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/users"
    
    # Validate inputs
    sort_field = inputs.get("sort_field")
    sort_direction = inputs.get("sort_direction")
    
    if not sort_field or not sort_direction:
        raise ValueError("Missing required input fields: sort_field and sort_direction")
    
    params = {
        "sort": sort_field,
        "order": sort_direction,
        "limit": 10
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty list, otherwise return the list
    users = data.get("users", [])
    
    if not users:
        return None
    
    return users