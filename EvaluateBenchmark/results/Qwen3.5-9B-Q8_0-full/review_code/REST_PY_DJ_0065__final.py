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
    # Extract included fields from inputs
    included_fields = inputs.get('included_fields', '')
    
    # Build the URL with query parameters for included fields
    base_url = 'https://dummyjson.com/users'
    params = {'include_fields': included_fields}
    
    try:
        response = requests.get(base_url, params=params)
        
        # Raise an exception for unsuccessful HTTP responses (status code not in 200-299)
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None for successful empty response
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")