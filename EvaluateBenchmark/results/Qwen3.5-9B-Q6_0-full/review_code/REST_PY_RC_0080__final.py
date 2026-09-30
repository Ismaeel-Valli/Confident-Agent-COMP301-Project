import requests

def solve(inputs):
    """
    Look up countries by exact match on their common country name using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The exact country name to match
            - results_to_skip: Number of results to skip (for pagination)
            - excluded_attributes: List of attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    results_to_skip = inputs["results_to_skip"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "name": value,
        "skip": results_to_skip
    }
    
    # Make the request with credentials in headers
    response = requests.get(
        base_url + "/v5.0/countries",
        params=params,
        headers={"Authorization": f"Bearer {credential}"}
    )
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # If empty response, return None
    if not data:
        return None
    
    # Filter out excluded attributes from each country object
    filtered_countries = []
    for country in data:
        filtered_country = {}
        for key, val in country.items():
            if key not in excluded_attributes:
                filtered_country[key] = val
        filtered_countries.append(filtered_country)
    
    return filtered_countries