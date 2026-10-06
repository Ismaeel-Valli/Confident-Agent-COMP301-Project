import requests

def solve(inputs):
    """
    Retrieves one page of products from DummyJSON API.
    
    Args:
        inputs (dict): A dictionary containing 'page' key with an integer value.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for empty response.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request is unsuccessful.
    """
    base_url = "https://dummyjson.com/products"
    page = inputs.get('page', 1)
    
    try:
        response = requests.get(f"{base_url}?page={page}")
        
        if response.status_code != 200:
            raise Exception(f"HTTP request failed with status code: {response.status_code}")
        
        data = response.json()
        
        # Check if the response is empty (no products found)
        if not data.get('products'):
            return None
            
        return data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")