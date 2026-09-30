def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The subregion to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip (for pagination)
            - excluded_attributes: List of country attributes to exclude from response
            - credential: Caller-supplied credential for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Base URL for REST Countries v5 API
    base_url = "https://api.restcountries.com"
    
    # Build the request URL with query parameters
    params = {
        'subregion': inputs['value'],
        'limit': inputs['result_limit'],
        'skip': inputs['results_to_skip']
    }
    
    # Make the API request with provided credential
    response = requests.get(
        base_url,
        params=params,
        headers={'Authorization': f'Bearer {inputs["credential"]}'}
    )
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    # Filter out excluded attributes from each country object
    if inputs['excluded_attributes']:
        filtered_data = []
        for country in data:
            filtered_country = {k: v for k, v in country.items() 
                             if k not in inputs['excluded_attributes']}
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data