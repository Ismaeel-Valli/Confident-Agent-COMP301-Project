import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON.
    
    Parameters:
        inputs (dict): Must contain 'page' key with an integer value.
    
    Returns:
        list or None: The decoded JSON response as a list, or None if the response is empty.
    
    Raises:
        requests.exceptions.RequestException: For unsuccessful HTTP responses.
    """
    page = inputs.get('page')
    if page is None:
        raise ValueError("Missing 'page' in inputs")
    
    base_url = "https://dummyjson.com/products"
    url = f"{base_url}?page={page}"
    
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    products = data.get('products', [])
    
    return products if products else None