def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Three-letter ISO country code to match exactly
            - result_limit: Maximum number of results
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Extract inputs
    iso_code = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the API URL for REST Countries v5
    # The endpoint for searching by ISO code is /v3.0/countries/{code}
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v3.0/countries/{iso_code}"
    
    # Prepare headers with the credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    if not response.ok:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    # Decode the JSON response
    try:
        data = response.json()
    except ValueError as e:
        raise Exception(f"Failed to decode JSON response: {e}")
    
    # Filter attributes if needed
    if included_attributes and isinstance(included_attributes, list):
        filtered_data = {}
        for attr in included_attributes:
            if attr in data:
                filtered_data[attr] = data[attr]
        return filtered_data
    
    return data