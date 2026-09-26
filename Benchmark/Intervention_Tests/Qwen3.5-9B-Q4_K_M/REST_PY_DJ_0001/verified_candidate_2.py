import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON and return the decoded JSON response.
    
    Args:
        inputs (dict): Must contain 'page' key with an integer value for pagination.
        
    Returns:
        dict or None: The decoded JSON response, or None if the response is empty.
        
    Raises:
        requests.exceptions.RequestException: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/products"
    page = inputs.get("page", 1)
    
    url = f"{base_url}?skip=0&limit=5&page={page}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise requests.exceptions.RequestException(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    return data if data else None