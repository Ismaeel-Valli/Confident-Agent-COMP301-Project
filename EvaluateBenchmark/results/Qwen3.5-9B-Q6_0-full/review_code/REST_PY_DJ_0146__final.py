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
    import requests
    
    base_url = "https://dummyjson.com/posts"
    sort_field = inputs["sort_field"]
    sort_direction = inputs["sort_direction"]
    
    params = {
        "limit": 1,
        "sort_by": sort_field,
        "order": sort_direction
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    # DummyJSON returns a dict with 'posts' key. If empty list, return None.
    if not data.get("posts"):
        return None
    
    return data