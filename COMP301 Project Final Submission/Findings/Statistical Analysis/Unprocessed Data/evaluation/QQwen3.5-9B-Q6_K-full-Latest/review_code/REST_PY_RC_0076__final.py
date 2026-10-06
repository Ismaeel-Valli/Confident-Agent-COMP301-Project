def solve(inputs):
    """
    Look up countries by exact match on their common country name using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The exact country name to search for
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Extract inputs
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Build the API URL with query parameters
    base_url = "https://api.restcountries.com/v5.0/countries"
    params = {
        "name": value,
        "limit": result_limit,
        "skip": results_to_skip
    }
    
    # Make the request with credential in headers
    response = requests.get(base_url, params=params, headers={"Authorization": f"Bearer {credential}"})
    
    # Check for unsuccessful HTTP response
    if not response.ok:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for empty successful response, otherwise return the data
    if len(data) == 0:
        return None
    
    return data