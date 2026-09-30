import requests

def solve(inputs):
    """
    Retrieves one page of products from DummyJSON based on the provided sort_field.
    
    Args:
        inputs (dict): A dictionary containing 'sort_field' key.
        
    Returns:
        list or None: The decoded JSON response as a list, or None if the response is empty.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://dummyjson.com/products"
    sort_field = inputs.get('sort_field')
    
    params = {
        'sort': sort_field,
        'skip': 0,
        'limit': 1
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise requests.exceptions.RequestException(f"HTTP error occurred: {response.status_code}")
    
    data = response.json()
    
    if not data.get('products'):
        return None
    
    return data['products']