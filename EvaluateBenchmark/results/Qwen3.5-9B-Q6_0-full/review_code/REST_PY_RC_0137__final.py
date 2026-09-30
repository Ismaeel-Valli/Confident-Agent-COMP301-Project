def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: The calling code to match exactly
            - result_limit: Maximum number of results to return
            - included_attributes: List of country attributes to include in response
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Build the API URL with exact match on calling code
    base_url = "https://api.restcountries.com/v5.0"
    url = f"{base_url}/country/calling-code/{inputs['value']}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    # Make the request
    response = requests.get(url, headers=headers)
    
    # Check for unsuccessful HTTP response
    if not response.ok:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for successful empty response
    if data is None or (isinstance(data, dict) and len(data) == 0):
        return None
    
    # Filter to only included attributes if specified
    if inputs['included_attributes']:
        filtered_data = {}
        for attr in inputs['included_attributes']:
            if attr in data:
                filtered_data[attr] = data[attr]
        return filtered_data
    
    return data