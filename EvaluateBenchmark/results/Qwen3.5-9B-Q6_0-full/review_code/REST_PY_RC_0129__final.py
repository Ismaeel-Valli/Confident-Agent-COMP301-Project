def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Currency code to match exactly
            - result_limit: Maximum number of results
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response (list of countries or None for empty)
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    base_url = "https://api.restcountries.com"
    currency_code = inputs["value"]
    limit = inputs["result_limit"]
    skip = inputs["results_to_skip"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the query parameters
    params = {
        "currency": currency_code,
        "limit": limit,
        "skip": skip,
        "fields": ",".join(attributes) if isinstance(attributes, list) else attributes
    }
    
    # Make the API request with credential
    headers = {"Authorization": f"Bearer {credential}"}
    response = requests.get(f"{base_url}/v5/countries", params=params, headers=headers)
    
    # Raise exception for unsuccessful HTTP response
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data