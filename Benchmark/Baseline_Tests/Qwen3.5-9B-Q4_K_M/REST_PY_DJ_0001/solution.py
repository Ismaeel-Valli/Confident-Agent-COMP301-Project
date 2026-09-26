import requests

def solve(inputs):
    """
    Retrieves one page of products from DummyJSON API.
    
    Args:
        inputs (dict): A dictionary containing 'page' key for pagination.
        
    Returns:
        list or None: Decoded JSON response as a list, or None if the response is empty.
        
    Raises:
        requests.RequestException: If the HTTP response is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    page = inputs.get('page', 1)
    
    url = f"{base_url}/products?page={page}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        if not data:
            return None
            
        return data
        
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to retrieve products: {e}") from e