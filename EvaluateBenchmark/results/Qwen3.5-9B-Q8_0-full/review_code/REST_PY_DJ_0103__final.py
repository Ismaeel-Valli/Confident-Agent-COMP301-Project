import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON with pagination support.
    
    Args:
        inputs (dict): Must contain 'result_limit' and 'sort_field'.
        
    Returns:
        dict or None: Decoded JSON response, or None if empty.
        
    Raises:
        requests.RequestException: If HTTP request fails.
    """
    base_url = "https://dummyjson.com/products"
    
    params = {
        "limit": inputs["result_limit"],
        "sort_by": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    if not data.get("products"):
        return None
    
    return data