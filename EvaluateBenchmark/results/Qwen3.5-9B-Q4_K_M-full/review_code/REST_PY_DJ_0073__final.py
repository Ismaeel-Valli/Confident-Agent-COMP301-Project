def solve(inputs):
    """
    Retrieve one page of products from DummyJSON, sorted by sort_field.
    
    Args:
        inputs (dict): Must contain 'sort_field' key with a string value.
        
    Returns:
        dict or None: The decoded JSON response if successful. Returns None for empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    base_url = "https://dummyjson.com/products"
    sort_field = inputs["sort_field"]
    
    url = f"{base_url}?sort=-{sort_field}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    return data