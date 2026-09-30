def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Three-letter ISO country code to match exactly
            - result_limit: Maximum number of results to return
            - included_attributes: List of attributes to include in the response
            - credential: Caller-supplied credential for authentication
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Extract inputs with validation
    value = inputs.get("value")
    result_limit = inputs.get("result_limit")
    included_attributes = inputs.get("included_attributes", [])
    credential = inputs.get("credential")
    
    if not value or len(value) != 3:
        raise ValueError("Value must be a three-letter ISO country code")
    
    # Build the API URL with query parameters
    base_url = "https://api.restcountries.com/v5.0"
    params = {
        "alpha": value,
        "limit": result_limit
    }
    
    # Add credential to headers if provided
    headers = {}
    if credential:
        headers["Authorization"] = f"Bearer {credential}"
    
    # Make the API request - use /country/{value} endpoint with params
    response = requests.get(f"{base_url}/country/{value}", params=params, headers=headers)
    
    # Check for unsuccessful HTTP response
    if not response.ok:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # If no countries found, return None
    if not data or len(data) == 0:
        return None
    
    # Filter to only include requested attributes
    if included_attributes:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in included_attributes:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data