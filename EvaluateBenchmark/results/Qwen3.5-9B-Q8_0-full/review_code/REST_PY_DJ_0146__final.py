import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON, sorted by sort_field in sort_direction.
    
    Args:
        inputs (dict): Must contain 'sort_field' and 'sort_direction'.
        
    Returns:
        list or None: Decoded JSON response as a list of posts, or None if empty.
        
    Raises:
        requests.RequestException: If HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/posts"
    
    # Validate inputs
    sort_field = inputs.get("sort_field")
    sort_direction = inputs.get("sort_direction")
    
    if not sort_field or not sort_direction:
        raise ValueError("inputs must contain 'sort_field' and 'sort_direction'")
    
    # Build query parameters using documented parameter names
    params = {
        "sort_by": sort_field,
        "order_by": sort_direction,
        "limit": 10  # Retrieve one page (default is 10)
    }
    
    response = requests.get(base_url, params=params)
    
    if not response.ok:
        raise requests.RequestException(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return the posts list or None if empty
    return data.get("posts")