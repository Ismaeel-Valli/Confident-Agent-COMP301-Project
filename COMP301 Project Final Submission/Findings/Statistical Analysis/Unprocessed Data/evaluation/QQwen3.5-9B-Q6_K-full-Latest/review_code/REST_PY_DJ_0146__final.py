import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON, sorted by sort_field in sort_direction.
    
    Args:
        inputs (dict): Must contain 'sort_field' and 'sort_direction'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/posts"
    
    # Validate inputs
    if 'sort_field' not in inputs or 'sort_direction' not in inputs:
        raise ValueError("inputs must contain 'sort_field' and 'sort_direction'")
    
    sort_field = inputs['sort_field']
    sort_direction = inputs['sort_direction']
    
    params = {
        'sort': sort_field,
        'order': sort_direction
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: status code {response.status_code}")
    
    data = response.json()
    
    # Return None for successful empty response (posts array is empty)
    if not data.get('posts'):
        return None
    
    return data