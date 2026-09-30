def solve(inputs):
    """
    Search country names using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip (offset)
            - excluded_attributes (list): Attributes to exclude from results
            - search_text (str): Search term for country names
            - credential (str): API credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Build the base URL for REST Countries v5
    base_url = "https://api.restcountries.com/v3.1"
    
    # Prepare query parameters
    params = {
        'search': inputs['search_text'],
        'skip': inputs['results_to_skip']
    }
    
    # Make the API request with the provided credential
    response = requests.get(base_url, params=params, headers={'Authorization': f'Bearer {inputs["credential"]}'})
    
    # Check for successful HTTP response
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for empty successful response, otherwise return the data
    if not data:
        return None
    
    return data