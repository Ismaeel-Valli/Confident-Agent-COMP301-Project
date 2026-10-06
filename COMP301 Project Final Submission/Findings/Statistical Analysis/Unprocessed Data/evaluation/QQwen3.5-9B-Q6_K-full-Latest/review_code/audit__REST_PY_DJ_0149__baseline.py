import requests

def solve(inputs):
    """
    Retrieves one page of products from DummyJSON based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip.
            - included_fields (str): Comma-separated list of fields to include.
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
    
    Raises:
        requests.RequestException: If the HTTP request is unsuccessful.
    """
    base_url = "https://dummyjson.com/products"
    
    # Parse included_fields into a list
    fields_list = [field.strip() for field in inputs['included_fields'].split(',')]
    
    params = {
        'limit': inputs['result_limit'],
        'skip': inputs['results_to_skip'],
        'select': ','.join(fields_list)
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise requests.RequestException(f"HTTP request failed with status code: {response.status_code}")
    
    data = response.json()
    
    # If the products list is empty, return None as per requirement
    if not data.get('products'):
        return None
    
    return data