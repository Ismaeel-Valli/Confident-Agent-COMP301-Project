import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON, sorted by sort_field in sort_direction.
    
    Args:
        inputs (dict): Must contain 'sort_field' and 'sort_direction'.
        
    Returns:
        dict or None: Decoded JSON response, or None if empty.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/products"
    
    params = {
        "skip": 0,
        "limit": 1,
        "sort_by": inputs["sort_field"],
        "sort_order": inputs["sort_direction"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data.get("products"):
        return None
    
    return data