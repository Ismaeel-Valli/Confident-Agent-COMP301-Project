def solve(inputs):
    """
    Look up countries by exact match on their calling code from REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The calling code to match exactly
            - included_attributes: List of attributes to include in response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Build the API URL with exact match on calling code
    base_url = "https://api.restcountries.com/v5.0"
    url = f"{base_url}/country/calling-code/{inputs['value']}"
    
    # Make the request with the provided credential
    response = requests.get(url, headers={"Authorization": inputs["credential"]})
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    # Filter to only included attributes if specified
    if inputs["included_attributes"]:
        filtered_data = {}
        for attr in inputs["included_attributes"]:
            if attr in data:
                filtered_data[attr] = data[attr]
        return filtered_data
    
    return data