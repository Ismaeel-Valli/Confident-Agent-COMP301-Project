def solve(inputs):
    """
    Look up countries by exact match on their bordering country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Country code to match exactly in borders
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of country attributes to exclude from response
            - credential: Caller-supplied credential (assumed valid)
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    base_url = "https://api.restcountries.com/v5.0"
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "borders": value,
        "limit": result_limit,
        "skip": results_to_skip
    }
    
    # Make the request with credentials in header
    headers = {"Authorization": f"Bearer {credential}"}
    
    response = requests.get(f"{base_url}/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    # Filter out excluded attributes if any
    if excluded_attributes:
        filtered_data = []
        for country in data:
            filtered_country = {k: v for k, v in country.items() if k not in excluded_attributes}
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data