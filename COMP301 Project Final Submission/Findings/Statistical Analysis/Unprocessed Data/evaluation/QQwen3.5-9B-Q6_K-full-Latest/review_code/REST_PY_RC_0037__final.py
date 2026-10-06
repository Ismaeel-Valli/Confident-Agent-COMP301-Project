def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - search_text (str): Search term for filtering countries
            - credential (str): Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Build the API URL with query parameters
    base_url = "https://api.restcountries.com/v5.0/countries"
    
    params = {
        'limit': inputs['result_limit'],
        'search': inputs['search_text']
    }
    
    # Make the request using the provided credential
    headers = {
        'Authorization': f'Bearer {inputs["credential"]}'
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode and return the JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data