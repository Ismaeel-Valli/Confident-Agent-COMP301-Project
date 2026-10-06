import requests

def solve(inputs):
    """
    Retrieve a product by identifier from DummyJSON.
    
    Args:
        inputs (dict): Must contain 'resource_id' key with the product ID.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        requests.exceptions.RequestException: For unsuccessful HTTP responses.
    """
    resource_id = inputs.get('resource_id')
    
    # DummyJSON products endpoint: https://dummyjson.com/products/{id}
    url = f"https://dummyjson.com/products/{resource_id}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data if data else None
    else:
        raise requests.exceptions.RequestException(f"HTTP {response.status_code}: {response.text}")