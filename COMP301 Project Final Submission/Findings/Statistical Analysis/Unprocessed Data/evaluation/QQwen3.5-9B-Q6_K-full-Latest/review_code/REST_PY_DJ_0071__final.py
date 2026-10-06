import requests

def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to return
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    # Base URL for DummyJSON todos endpoint
    base_url = "https://dummyjson.com/todos"
    
    # Parse included_fields from comma-separated string
    if not inputs.get('included_fields'):
        included_fields = []
    else:
        included_fields = [field.strip() for field in inputs['included_fields'].split(',')]
    
    # Build query parameters for filtering fields
    params = {}
    if included_fields:
        params['include'] = ','.join(included_fields)
    
    # Make the GET request
    response = requests.get(base_url, params=params)
    
    # Raise exception for unsuccessful HTTP responses
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for empty successful response (no todos)
    if not data.get('todos') or len(data['todos']) == 0:
        return None
    
    return data