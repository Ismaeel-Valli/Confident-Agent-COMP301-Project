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
    sort_field = inputs.get('sort_field')
    
    # DummyJSON users endpoint with sorting
    url = f"https://dummyjson.com/users?sort={sort_field}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    # Return the users list or None if empty
    return data.get('users')