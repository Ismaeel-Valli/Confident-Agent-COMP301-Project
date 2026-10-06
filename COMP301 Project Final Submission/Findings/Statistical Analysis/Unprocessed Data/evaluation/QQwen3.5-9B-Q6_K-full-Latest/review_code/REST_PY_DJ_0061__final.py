import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - 'included_fields' (str): Comma-separated list of fields to include
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/products"
    
    # Parse included_fields from comma-separated string
    if inputs.get('included_fields'):
        fields = [f.strip() for f in inputs['included_fields'].split(',')]
        params = {'include': ','.join(fields)}
    else:
        params = {}
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data.get('products'):
        return None
    
    return data