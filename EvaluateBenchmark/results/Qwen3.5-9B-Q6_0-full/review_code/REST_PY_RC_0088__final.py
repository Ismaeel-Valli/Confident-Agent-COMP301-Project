def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: The region to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - credential: Caller-supplied authentication credential
    
    Returns:
        list or None: Decoded JSON response as a list, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    base_url = "https://api.restcountries.com"
    region = inputs["value"]
    limit = inputs["result_limit"]
    skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "region": region,
        "limit": limit,
        "skip": skip
    }
    
    # Make the API request with credentials in header
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(base_url + "/v5.0/countries", params=params, headers=headers)
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None for empty successful response
    if len(data) == 0:
        return None
    
    return data