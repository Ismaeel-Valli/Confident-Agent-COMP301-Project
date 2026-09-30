def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The three-letter ISO country code to match exactly
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Extract inputs
    iso_code = inputs["value"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the API URL with query parameters
    base_url = "https://api.restcountries.com/v5.0"
    url = f"{base_url}/country/{iso_code}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers)
    
    # Check for successful HTTP status
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for empty response, otherwise return the data
    if not data:
        return None
    
    # Filter attributes if specified
    if attributes:
        filtered_data = {}
        for attr in attributes:
            if attr in data:
                filtered_data[attr] = data[attr]
        return filtered_data
    
    return data