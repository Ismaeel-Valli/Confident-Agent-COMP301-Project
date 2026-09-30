def solve(inputs):
    """
    Look up countries by exact match on their common country name using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The exact country name to match
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip (pagination)
            - excluded_attributes: List of attributes to exclude from results
            - credential: Caller-supplied credential for authentication
    
    Returns:
        list or None: Decoded JSON response as a list, or None if empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Base URL for REST Countries v5 API
    base_url = "https://api.restcountries.com/v5.0"
    
    # Build the request URL with query parameters
    params = {
        'name': inputs['value'],
        'limit': inputs['result_limit'],
        'skip': inputs['results_to_skip']
    }
    
    # Make the GET request
    response = requests.get(
        base_url,
        params=params,
        headers={'Authorization': f'Bearer {inputs["credential"]}'}
    )
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # If the response is empty, return None
    if not data:
        return None
    
    # Exclude specified attributes from each country object
    excluded_attrs = inputs.get('excluded_attributes', [])
    filtered_data = []
    
    for country in data:
        filtered_country = {k: v for k, v in country.items() if k not in excluded_attrs}
        filtered_data.append(filtered_country)
    
    return filtered_data