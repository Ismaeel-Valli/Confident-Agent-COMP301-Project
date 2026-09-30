def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Currency code to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of country attributes to exclude from each result
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    base_url = "https://api.restcountries.com/v5"
    
    # Build the query parameters
    params = {
        "currency": inputs["value"],
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    # Make the request with the provided credential
    headers = {"Authorization": f"Bearer {inputs['credential']}"}
    response = requests.get(f"{base_url}/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # Filter out excluded attributes from each country object
    if data:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for key, value in country.items():
                if key not in inputs["excluded_attributes"]:
                    filtered_country[key] = value
            filtered_data.append(filtered_country)
        return filtered_data
    
    return None