def solve(inputs):
    """
    Retrieve one page of products from DummyJSON and return the decoded JSON response.
    
    Args:
        inputs (dict): Must contain 'post_id' key with an integer value representing the product ID.
        
    Returns:
        dict or None: The decoded JSON response, or None if the response is empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses (status code not in 200-299).
    """
    import requests
    
    base_url = "https://dummyjson.com/products"
    endpoint = f"/{inputs['post_id']}"
    url = base_url + endpoint
    
    response = requests.get(url)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    return data if data else None