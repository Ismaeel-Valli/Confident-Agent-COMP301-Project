import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON with sorting.
    
    Args:
        inputs (dict): Must contain 'sort_field' and 'sort_direction'.
        
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/products"
    
    # Validate inputs
    if not isinstance(inputs, dict):
        raise ValueError("inputs must be a dictionary")
    
    sort_field = inputs.get('sort_field')
    sort_direction = inputs.get('sort_direction')
    
    if sort_field is None:
        raise ValueError("Missing required parameter: sort_field")
    if sort_direction is None:
        raise ValueError("Missing required parameter: sort_direction")
    
    # Build query parameters - only use documented ones
    params = {}
    if sort_field:
        params['sort_by'] = sort_field
    if sort_direction:
        params['order'] = sort_direction
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response (no products found)
    if not data.get('products'):
        return None
    
    return data