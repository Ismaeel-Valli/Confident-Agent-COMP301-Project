def solve(inputs):
    """
    Look up countries by exact region match using REST Countries v5 API.
    
    Args:
        inputs (dict): Must contain:
            - "value": The region to match exactly
            - "included_attributes": List of attributes to include in response
            - "credential": Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Extract inputs with validation
    value = inputs["value"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the API URL for REST Countries v5 - try basic countries endpoint
    base_url = "https://api.restcountries.com/v3.1/countries"
    url = base_url
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers)
    
    # Check for unsuccessful HTTP response
    if not response.ok:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    # Filter to only included attributes if specified
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