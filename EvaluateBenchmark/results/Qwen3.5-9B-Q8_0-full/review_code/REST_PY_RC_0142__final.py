import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code from REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: The calling code to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of country attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    calling_code = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build the API endpoint for exact match on calling code
    url = f"{base_url}/v5.1/calling-code/{calling_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
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
    
    # If the response is an empty list or None, return None as per spec
    if data is None or (isinstance(data, list) and len(data) == 0):
        return None
    
    # Filter out excluded attributes from each country object
    filtered_countries = []
    for country in data:
        filtered_country = {}
        for key, value in country.items():
            if key not in excluded_attributes:
                filtered_country[key] = value
        filtered_countries.append(filtered_country)
    
    return filtered_countries