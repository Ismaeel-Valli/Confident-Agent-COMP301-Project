def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Currency code to match exactly
            - result_limit: Maximum number of results
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of country attributes to exclude
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Base URL for REST Countries v5 API
    base_url = "https://api.restcountries.com/v5.0"
    
    # Build the query parameters
    params = {
        "currency": inputs["value"],
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    # Make the API request with the provided credential
    response = requests.get(
        f"{base_url}/countries",
        params=params,
        headers={"Authorization": f"Bearer {inputs['credential']}"}
    )
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    # Exclude specified attributes from each country object
    excluded_attrs = inputs.get("excluded_attributes", [])
    filtered_countries = []
    
    for country in data:
        filtered_country = {k: v for k, v in country.items() if k not in excluded_attrs}
        filtered_countries.append(filtered_country)
    
    return filtered_countries