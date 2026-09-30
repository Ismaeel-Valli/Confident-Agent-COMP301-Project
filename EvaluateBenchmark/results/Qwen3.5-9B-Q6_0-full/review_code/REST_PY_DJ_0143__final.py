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
    
    params = {
        "sort": inputs["sort_field"],
        "order": inputs["sort_direction"]
    }
    
    response = requests.get(base_url, params=params)
    
    if not response.ok:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    users = data.get("users", [])
    
    return None if len(users) == 0 else users