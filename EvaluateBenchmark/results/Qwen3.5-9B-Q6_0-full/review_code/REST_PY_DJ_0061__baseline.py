import requests

def solve(inputs):
    """
    Retrieves one page of products from DummyJSON based on included_fields.
    
    Args:
        inputs (dict): A dictionary containing 'included_fields' as a comma-separated string.
        
    Returns:
        dict or None: The decoded JSON response, or None if the response is empty but successful.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    # Extract included_fields from inputs
    included_fields = inputs.get('included_fields', '')
    
    # Construct the API URL with query parameters for fields and page
    base_url = "https://dummyjson.com/products"
    params = {
        'include': included_fields,
        'page': 1
    }
    
    try:
        response = requests.get(base_url, params=params)
        
        # Raise an exception for unsuccessful HTTP responses (status code outside 200-299)
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None if the products list is empty, otherwise return the full response
        if not data.get('products'):
            return None
            
        return data
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Unsuccessful HTTP response: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")