import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON, skipping a specified number of results.
    
    Args:
        inputs (dict): Must contain 'results_to_skip' (int).
        
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://dummyjson.com/products"
    skip = inputs.get("results_to_skip", 0)
    
    # Build query parameters
    params = {"skip": skip, "limit": 1}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Return None for successful empty response (empty array)
        if not data.get("products"):
            return None
            
        return data
        
    except requests.RequestException as e:
        raise e