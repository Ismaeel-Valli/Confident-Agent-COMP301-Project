import requests

def solve(inputs):
    """
    Retrieves one page of products from DummyJSON based on the provided sort_field.
    
    Args:
        inputs (dict): A dictionary containing 'sort_field' key.
        
    Returns:
        list or None: The decoded JSON response as a list of products, or None if the response is empty.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://dummyjson.com/products"
    sort_field = inputs.get('sort_field')
    
    params = {'sort': sort_field}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        products = data.get('products', [])
        
        if not products:
            return None
            
        return products
        
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"HTTP request failed: {e}")