def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The three-letter ISO country code to match exactly
            - result_limit: Maximum number of results to return
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        list or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Extract inputs
    iso_code = inputs["value"]
    limit = inputs["result_limit"]
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
    
    # Raise exception for unsuccessful HTTP responses
    if not response.ok:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for empty successful response, otherwise return the data
    if data is None or len(data) == 0:
        return None
    
    return data