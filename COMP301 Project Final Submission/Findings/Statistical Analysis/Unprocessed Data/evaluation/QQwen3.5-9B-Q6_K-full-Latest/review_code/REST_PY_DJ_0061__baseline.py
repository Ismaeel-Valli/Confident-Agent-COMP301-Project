import requests

def solve(inputs):
    """
    Retrieves one page of products from DummyJSON based on included_fields.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'included_fields' (str): Comma-separated list of fields to include in the response.
    
    Returns:
        dict or None: The decoded JSON response if successful, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/products"
    included_fields = inputs.get('included_fields', '')
    
    # Prepare query parameters
    params = {}
    if included_fields:
        params['include'] = included_fields
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # DummyJSON returns a list of products directly at the root level for this endpoint
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as errh:
        raise Exception(f"HTTP Error occurred: {errh}")
    except requests.exceptions.RequestException as err:
        raise Exception(f"Request failed: {err}")