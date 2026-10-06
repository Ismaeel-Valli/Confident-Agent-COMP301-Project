import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON, sorted by sort_field.
    
    Args:
        inputs (dict): Must contain 'sort_field' key.
        
    Returns:
        list or None: Decoded JSON response as a list, or None if empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users"
    sort_field = inputs.get("sort_field")
    
    params = {"sort": sort_field}
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    data = response.json()
    users = data.get("users", [])
    
    if not users:
        return None
    
    return users