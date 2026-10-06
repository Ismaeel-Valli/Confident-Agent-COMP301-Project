import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON.
    
    Args:
        inputs (dict): Must contain 'page' key with an integer value.
        
    Returns:
        dict or None: Decoded JSON response, or None if empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    page = inputs.get('page')
    if page is None:
        raise ValueError("Missing 'page' in inputs")
    
    base_url = "https://dummyjson.com/products"
    url = f"{base_url}?page={page}"
    
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    return data