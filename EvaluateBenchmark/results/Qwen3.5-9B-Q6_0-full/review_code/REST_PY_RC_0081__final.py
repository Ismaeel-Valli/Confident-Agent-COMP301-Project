def solve(inputs):
    """
    Look up countries by exact match on their common country name using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The exact country name to match
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip (pagination)
            - included_attributes: List of attributes to include in response
            - credential: Caller-supplied credential for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
        Raises: Exception for unsuccessful HTTP responses
    """
    import requests
    
    # Base URL for REST Countries v5 API
    base_url = "https://api.restcountries.com/v5.0"
    
    # Build the request URL with query parameters
    params = {
        "name": inputs["value"],
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    # Make the GET request with credentials in headers
    response = requests.get(
        f"{base_url}/countries",
        params=params,
        headers={"Authorization": f"Bearer {inputs['credential']}"}
    )
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # If successful but empty, return None
    if not data:
        return None
    
    # Filter to only include requested attributes
    if inputs["included_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in inputs["included_attributes"]:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data