import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON with specified included fields.
    
    Args:
        inputs (dict): Dictionary containing 'included_fields' (comma-separated string)
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    # Extract included fields from inputs
    included_fields = inputs.get('included_fields', '')
    
    # Build the URL with query parameters for included fields
    base_url = "https://dummyjson.com/users"
    params = {}
    
    if included_fields:
        params['include'] = included_fields
    
    # Make the GET request
    response = requests.get(base_url, params=params)
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None for successful empty response (empty users array)
    if not data.get('users'):
        return None
    
    return data