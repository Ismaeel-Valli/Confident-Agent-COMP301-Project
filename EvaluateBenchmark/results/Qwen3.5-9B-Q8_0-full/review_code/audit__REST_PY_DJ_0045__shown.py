import requests

def solve(inputs):
    """
    Retrieve a product by identifier from DummyJSON and return its title.
    
    Args:
        inputs (dict): Must contain 'resource_id' key with the product ID.
        
    Returns:
        str or None: The product's title, or None if absent or response is empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful (non-2xx status).
    """
    resource_id = inputs.get("resource_id")
    
    # DummyJSON products endpoint: https://dummyjson.com/products/<id>
    url = f"https://dummyjson.com/products/{resource_id}"
    
    try:
        response = requests.get(url)
        
        # Raise an exception for unsuccessful HTTP responses (non-2xx)
        response.raise_for_status()
        
        data = response.json()
        
        # Return title if present, otherwise None
        return data.get("title")
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")