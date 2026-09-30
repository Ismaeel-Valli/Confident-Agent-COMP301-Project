def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The three-letter ISO country code to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to include in the response
            - credential: Caller-supplied credential (assumed to have necessary permissions)
    
    Returns:
        list or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    # Extract inputs
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the API URL for REST Countries v5 (exact match on 3-letter ISO code)
    base_url = "https://api.restcountries.com/v5.0/countries"
    url = f"{base_url}?iso2={value}"
    
    # Make the request with the credential
    headers = {"Authorization": f"Bearer {credential}"}
    response = requests.get(url, headers=headers)
    
    # Check for unsuccessful HTTP response
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code}")
    
    # Decode the JSON response
    data = response.json()
    
    # If no results found, return None (successful empty response)
    if not data or len(data) == 0:
        return None
    
    # Filter to only include requested attributes
    filtered_results = []
    for country in data:
        filtered_country = {}
        for attr in included_attributes:
            if attr in country:
                filtered_country[attr] = country[attr]
        filtered_results.append(filtered_country)
    
    # Apply pagination limits
    start_index = results_to_skip
    end_index = min(start_index + result_limit, len(filtered_results))
    
    return filtered_results[start_index:end_index]