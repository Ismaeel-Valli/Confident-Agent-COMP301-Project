def solve(inputs):
    """
    Look up countries by exact match on their bordering country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Country code to match exactly in borders
            - result_limit: Maximum number of results
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of attributes to exclude from results
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    base_url = "https://api.restcountries.com"
    endpoint = "/v5.1/countries/borders/{code}"
    
    value = inputs["value"]
    result_limit = inputs.get("result_limit", 10)
    results_to_skip = inputs.get("results_to_skip", 0)
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    url = base_url + endpoint.replace("{code}", value)
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    params = {}
    if result_limit is not None:
        params["limit"] = result_limit
    if results_to_skip is not None:
        params["skip"] = results_to_skip
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Filter out excluded attributes if any
    if excluded_attributes:
        filtered_data = {}
        for key, val in data.items():
            if key not in excluded_attributes:
                filtered_data[key] = val
        return filtered_data
    
    return data