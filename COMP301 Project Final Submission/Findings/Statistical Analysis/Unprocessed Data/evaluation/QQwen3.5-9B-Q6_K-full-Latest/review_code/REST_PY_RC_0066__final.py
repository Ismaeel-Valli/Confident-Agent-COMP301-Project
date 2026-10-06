def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The three-letter ISO country code to match exactly
            - results_to_skip: Number of results to skip (for pagination)
            - included_attributes: List of attributes to return for each country
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
    """
    import requests
    
    # Base URL for REST Countries v5 API
    base_url = "https://api.restcountries.com/v5.0"
    
    # Build the query parameters
    params = {
        "code": inputs["value"],
        "skip": inputs["results_to_skip"]
    }
    
    # Make the GET request with the provided credential
    response = requests.get(
        base_url,
        params=params,
        headers={"Authorization": f"Bearer {inputs['credential']}"}
    )
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # If the response is empty (successful but no results), return None
    if not data:
        return None
    
    # Filter to only include the requested attributes
    if inputs["included_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in inputs["included_attributes"]:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    # Return the full response as-is
    return data