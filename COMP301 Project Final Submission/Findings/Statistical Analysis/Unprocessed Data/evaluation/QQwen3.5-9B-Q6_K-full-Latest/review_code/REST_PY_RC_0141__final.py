def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The calling code to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to include in the response
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Build the API URL with query parameters
    base_url = "https://api.restcountries.com/v5.0"
    
    params = {
        'code': inputs['value'],
        'limit': inputs['result_limit'],
        'skip': inputs['results_to_skip']
    }
    
    # Make the API request with the provided credential
    response = requests.get(base_url, params=params)
    
    # Check for unsuccessful HTTP response
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    # Decode the JSON response
    data = response.json()
    
    # If no results found, return None
    if not data or len(data) == 0:
        return None
    
    # Filter to only include requested attributes
    included_attributes = inputs.get('included_attributes', [])
    filtered_results = []
    
    for country in data:
        filtered_country = {}
        for attr in included_attributes:
            if attr in country:
                filtered_country[attr] = country[attr]
        filtered_results.append(filtered_country)
    
    return filtered_results