import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON with pagination.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip.
    
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/products"
    result_limit = inputs.get("result_limit")
    results_to_skip = inputs.get("results_to_skip")
    
    params = {}
    if result_limit is not None:
        params["limit"] = result_limit
    if results_to_skip is not None:
        params["skip"] = results_to_skip
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    # DummyJSON returns a dict with a "products" key.
    # If the products list is empty, return None.
    if not data.get("products"):
        return None
    
    return data