def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The calling code to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to include in the response
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    base_url = "https://api.restcountries.com"
    calling_code = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the query parameters
    params = {
        "callingcode": calling_code,
        "limit": result_limit,
        "skip": results_to_skip,
        "fields": ",".join(included_attributes) if included_attributes else None
    }
    
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}
    
    # Make the API request with credential
    headers = {"Authorization": f"Bearer {credential}"}
    response = requests.get(f"{base_url}/v5.0/countries", params=params, headers=headers)
    
    # Raise exception for unsuccessful HTTP response
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data