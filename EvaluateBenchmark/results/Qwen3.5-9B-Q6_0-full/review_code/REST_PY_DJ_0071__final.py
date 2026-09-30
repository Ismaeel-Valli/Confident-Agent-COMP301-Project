import requests

def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON with specified included fields.
    
    Args:
        inputs (dict): Dictionary containing:
            - 'included_fields' (str): Comma-separated list of fields to include
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    # Base URL for DummyJSON todos endpoint
    base_url = "https://dummyjson.com/todos"
    
    # Parse included fields from comma-separated string
    included_fields = inputs.get('included_fields', '')
    if included_fields:
        fields_list = [f.strip() for f in included_fields.split(',')]
        params = {
            'include': ','.join(fields_list)
        }
    else:
        params = {}
    
    # Make the GET request
    response = requests.get(base_url, params=params)
    
    # Raise exception for unsuccessful HTTP response
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    # Decode and return JSON response
    data = response.json()
    
    # Return None for empty successful response
    if not data.get('todos'):
        return None
    
    return data