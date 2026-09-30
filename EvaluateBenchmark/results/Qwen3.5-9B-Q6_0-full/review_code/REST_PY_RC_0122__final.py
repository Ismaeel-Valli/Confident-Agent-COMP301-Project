def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Currency code to match exactly
            - included_attributes: List of attributes to return for each country
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
    """
    import requests
    
    # Build the API URL with currency parameter
    base_url = "https://api.restcountries.com/v5.0"
    url = f"{base_url}/currency/{inputs['value']}"
    
    # Make the request with the provided credential
    response = requests.get(url, headers={"Authorization": inputs["credential"]})
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None if the response is empty (successful but no results)
    if not data:
        return None
    
    # Filter to only include requested attributes if specified
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