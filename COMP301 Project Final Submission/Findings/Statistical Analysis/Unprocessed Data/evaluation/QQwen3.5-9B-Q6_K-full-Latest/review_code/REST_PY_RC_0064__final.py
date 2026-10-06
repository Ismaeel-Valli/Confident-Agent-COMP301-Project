def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Three-letter ISO country code to match exactly
            - result_limit: Maximum number of results to return
            - excluded_attributes: List of country attributes to exclude from response
            - credential: Caller-supplied credential for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Extract inputs with validation
    value = inputs.get("value")
    result_limit = inputs.get("result_limit")
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs.get("credential")
    
    if not value:
        raise ValueError("Missing required 'value' parameter")
    
    # Build the API URL for REST Countries v5 - use /country/{code} endpoint
    base_url = "https://api.restcountries.com/v5.0"
    url = f"{base_url}/country/{value}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    # Make the API request
    response = requests.get(url, headers=headers)
    
    # Check HTTP status
    if not response.ok:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Filter out excluded attributes if any (without mutating original data)
    if excluded_attributes:
        filtered_data = {}
        for key, val in data.items():
            if key not in excluded_attributes:
                filtered_data[key] = val
        return filtered_data
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data