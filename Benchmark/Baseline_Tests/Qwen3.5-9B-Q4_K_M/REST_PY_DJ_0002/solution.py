import requests

def solve(inputs):
    """
    Retrieves a product by identifier from DummyJSON.
    
    Args:
        inputs (dict): A dictionary containing 'resource_id' as the product identifier.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    resource_id = inputs.get('resource_id')
    
    # DummyJSON endpoint to get a product by ID
    url = f"https://dummyjson.com/products/{resource_id}"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return None if not data else data
        elif response.status_code == 404:
            # Assuming this means the product was found but has no details or is intentionally empty
            return None
        else:
            raise Exception(f"HTTP Error {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")