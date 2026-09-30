import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON with specified included fields.
    
    Args:
        inputs (dict): Dictionary containing:
            - 'included_fields': str, comma-separated list of fields to include
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/users"
    
    # Parse included_fields from comma-separated string
    if 'included_fields' not in inputs:
        raise ValueError("Missing required key 'included_fields' in inputs")
    
    included_fields = inputs['included_fields']
    
    # Build query parameters for fields to include
    params = {'include_fields': included_fields}
    
    try:
        response = requests.get(base_url, params=params)
        
        if response.status_code != 200:
            raise Exception(f"HTTP error: {response.status_code}")
        
        data = response.json()
        
        # Return None for empty successful response
        if not data.get('users'):
            return None
        
        return data
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")