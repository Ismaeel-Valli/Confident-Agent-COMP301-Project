def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The two-letter ISO country code to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to include in the response
            - credential: Caller-supplied credential (assumed to have necessary permissions)
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Base URL for REST Countries v5 API
    base_url = "https://api.restcountries.com/v5"
    
    # Build the request URL with query parameters
    url = f"{base_url}/country/{inputs['value']}"
    
    # Prepare headers with the credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers)
    
    # Check for successful HTTP response
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    # Decode the JSON response
    data = response.json()
    
    # If the response is empty (no countries found), return None
    if not data:
        return None
    
    # Filter to only include the requested attributes
    included_attributes = inputs['included_attributes']
    filtered_results = []
    
    for country in data:
        filtered_country = {}
        for attr in included_attributes:
            if attr in country:
                filtered_country[attr] = country[attr]
        filtered_results.append(filtered_country)
    
    # Apply pagination (skip and limit)
    start_index = inputs['results_to_skip']
    end_index = start_index + inputs['result_limit']
    
    return filtered_results[start_index:end_index]