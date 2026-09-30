import requests

def solve(inputs):
    """
    Retrieve a product by identifier from DummyJSON.
    
    Args:
        inputs (dict): Must contain 'resource_id' key with the product identifier.
        
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    url = f"https://dummyjson.com/products/{resource_id}"
    
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for unsuccessful HTTP status codes
    
    if response.status_code == 204:
        return None
    
    return response.json()