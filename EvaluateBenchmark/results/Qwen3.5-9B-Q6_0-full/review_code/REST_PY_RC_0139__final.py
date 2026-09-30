def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: The calling code to match exactly
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to include in response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    base_url = "https://api.restcountries.com"
    calling_code = inputs["value"]
    skip = inputs["results_to_skip"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the query parameters
    params = {
        "callingcode": calling_code,
        "skip": skip,
        "fields": ",".join(attributes)
    }
    
    # Make the API request with authentication
    response = requests.get(
        base_url + "/v5",
        params=params,
        headers={"Authorization": f"Bearer {credential}"}
    )
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    result = response.json()
    
    # Return None for successful empty response
    if not result:
        return None
    
    return result