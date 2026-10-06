def solve(inputs):
    """
    Look up countries by exact match on their bordering country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Country code to match exactly (str)
            - result_limit: Maximum number of results (int)
            - results_to_skip: Number of results to skip (int)
            - included_attributes: List of attributes to include (list)
            - credential: Caller-supplied credential (str)
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    base_url = "https://api.restcountries.com/v5.0"
    endpoint = "/borders"
    
    params = {
        "value": inputs["value"],
        "result_limit": inputs["result_limit"],
        "results_to_skip": inputs["results_to_skip"]
    }
    
    if inputs["included_attributes"]:
        params["included_attributes"] = ",".join(inputs["included_attributes"])
    
    response = requests.get(f"{base_url}{endpoint}", params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    return data if data else None