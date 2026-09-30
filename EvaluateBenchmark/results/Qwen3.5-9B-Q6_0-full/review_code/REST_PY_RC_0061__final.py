def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - included_attributes (list): List of country attributes to include
            - search_text (str): Search term for filtering countries
            - credential (str): Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Build the base URL for REST Countries v5 API
    base_url = "https://api.restcountries.com/v5.0/countries"
    
    # Prepare parameters
    params = {
        'limit': inputs['result_limit'],
        'search': inputs.get('search_text', ''),
        'fields': ','.join(inputs['included_attributes']) if inputs['included_attributes'] else None
    }
    
    # Make the API request with provided credential
    headers = {
        'Authorization': f'Bearer {inputs["credential"]}'
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    # Raise exception for unsuccessful HTTP response
    if not response.ok:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data