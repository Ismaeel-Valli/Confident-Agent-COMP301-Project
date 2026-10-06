import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON, sorted by sort_field.
    
    Args:
        inputs (dict): Must contain 'sort_field' key.
        
    Returns:
        list or None: Decoded JSON response (list of products), or None if empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/products"
    sort_field = inputs.get("sort_field")
    
    params = {"sortBy": sort_field}
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    products = data.get("products", [])
    
    return products if products else None