import requests

def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The subregion to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of attributes to exclude from results
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    subregion = inputs["value"]
    limit = inputs["result_limit"]
    skip = inputs["results_to_skip"]
    excluded_attrs = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "subregion": subregion,
        "limit": limit,
        "skip": skip
    }
    
    # Make the request with credentials in header
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(f"{base_url}/v5/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If empty response, return None as per spec
    if not data:
        return None
    
    # Filter out excluded attributes from each country object
    filtered_results = []
    for country in data:
        filtered_country = {}
        for key, value in country.items():
            if key not in excluded_attrs:
                filtered_country[key] = value
        filtered_results.append(filtered_country)
    
    return filtered_results