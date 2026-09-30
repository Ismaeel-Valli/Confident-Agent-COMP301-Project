def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: The subregion to match exactly
            - result_limit: Maximum number of results to return
            - included_attributes: List of country attributes to include in response
            - credential: Caller-supplied credential for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty response
        Raises: Exception for unsuccessful HTTP responses
    """
    import requests
    
    # Build the API URL with query parameters
    base_url = "https://api.restcountries.com/v5.0"
    
    # Construct the request URL with subregion parameter and limit
    url = f"{base_url}/subregion/{inputs['value']}?limit={inputs['result_limit']}"
    
    # Make the authenticated request
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    # Check for unsuccessful HTTP response
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    # Decode the JSON response
    data = response.json()
    
    # If successful but empty response, return None
    if not data:
        return None
    
    # Filter to only include requested attributes
    if inputs['included_attributes']:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in inputs['included_attributes']:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data