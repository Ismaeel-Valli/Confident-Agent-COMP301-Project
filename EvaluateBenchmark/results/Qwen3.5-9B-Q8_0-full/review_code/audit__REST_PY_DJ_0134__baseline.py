import requests

def solve(inputs):
    """
    Retrieves one page of users from DummyJSON based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'included_fields' (str): Comma-separated list of fields to return.
            - 'sort_field' (str): Field used for ordering.
    
    Returns:
        dict or None: Decoded JSON response if successful, or None if the response is empty.
    
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = "/users"
    
    # Construct query parameters
    params = {}
    if inputs.get('included_fields'):
        params['fields'] = inputs['included_fields']
    if inputs.get('sort_field'):
        params['sort'] = inputs['sort_field']
    
    try:
        response = requests.get(f"{base_url}{endpoint}", params=params)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # Return None if the response is empty (successful but no data)
        if not data:
            return None
            
        return data
    
    except requests.RequestException as e:
        raise e