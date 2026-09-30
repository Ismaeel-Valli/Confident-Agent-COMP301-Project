def solve(inputs):
    """
    Look up countries by exact match on their bordering country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Country code to match exactly (str)
            - result_limit: Maximum number of results (int)
            - included_attributes: List of attributes to include in response (list)
            - credential: Caller-supplied credential (str)
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Base URL for REST Countries v5 API
    base_url = "https://api.restcountries.com/v5"
    
    # Build the request URL with the bordering country code parameter
    url = f"{base_url}/borders/{inputs['value']}"
    
    # Prepare headers with the credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # If the response is empty (successful but no results), return None
    if not data:
        return None
    
    # Filter the response to include only the requested attributes
    if inputs['included_attributes']:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in inputs['included_attributes']:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    # Return the full response if no attributes were specified
    return data