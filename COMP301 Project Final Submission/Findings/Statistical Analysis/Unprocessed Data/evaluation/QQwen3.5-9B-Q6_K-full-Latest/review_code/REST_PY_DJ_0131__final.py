import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to include
            - sort_field (str): Field to sort by
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/products"
    
    # Build query parameters
    params = {}
    
    if inputs.get("included_fields"):
        params["include"] = inputs["included_fields"]
    
    if inputs.get("sort_field"):
        params["sort"] = inputs["sort_field"]
    
    response = requests.get(base_url, params=params)
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    data = response.json()
    
    # Return None for empty successful response
    if not data.get("products"):
        return None
    
    return data