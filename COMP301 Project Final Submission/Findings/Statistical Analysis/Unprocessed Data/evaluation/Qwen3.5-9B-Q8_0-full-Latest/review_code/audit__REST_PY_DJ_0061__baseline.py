import requests

def solve(inputs):
    """
    Retrieves one page of products from DummyJSON based on included_fields.
    
    Args:
        inputs (dict): Dictionary containing 'included_fields' as a comma-separated string.
        
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty but successful.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    included_fields = inputs.get('included_fields', '')
    
    # Construct the URL with query parameters for fields
    url = "https://dummyjson.com/products?include_fields=" + included_fields
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # Check if the response is empty (e.g., products list is empty)
        if not data.get('products'):
            return None
            
        return data
        
    except requests.exceptions.HTTPError as errh:
        raise Exception(f"HTTP Error occurred: {errh}")
    except requests.exceptions.RequestException as err:
        raise Exception(f"Request failed: {err}")