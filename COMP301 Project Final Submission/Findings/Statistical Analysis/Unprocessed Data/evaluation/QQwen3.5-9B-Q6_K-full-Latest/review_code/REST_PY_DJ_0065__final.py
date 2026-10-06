import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON with specified included fields.
    
    Args:
        inputs (dict): Dictionary containing:
            - 'included_fields' (str): Comma-separated list of fields to include
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/users"
    
    # Parse included_fields from comma-separated string
    included_fields = inputs.get('included_fields', '')
    
    # Build query parameters if fields are specified
    params = {}
    if included_fields:
        params['include_fields'] = included_fields
    
    try:
        response = requests.get(base_url, params=params)
        
        # Raise exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode JSON response
        data = response.json()
        
        # Return None for successful empty response
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")