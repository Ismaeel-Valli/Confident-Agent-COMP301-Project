import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON, skipping a specified number of results.
    
    Args:
        inputs (dict): Dictionary containing 'results_to_skip' key with an integer value.
        
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/products"
    skip = inputs.get("results_to_skip", 0)
    
    params = {
        "skip": skip,
        "limit": 1
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    # Return None for empty products array
    if not data.get("products"):
        return None
    
    return data