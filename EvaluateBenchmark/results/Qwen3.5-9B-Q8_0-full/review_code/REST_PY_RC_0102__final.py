import requests

def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The subregion to match exactly
            - result_limit: Maximum number of results to return
            - excluded_attributes: List of country attributes to exclude from results
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    subregion = inputs["value"]
    limit = inputs["result_limit"]
    excluded_attrs = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "subregion": subregion,
        "limit": limit
    }
    
    # Make the API request with credentials in header
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(f"{base_url}/v5.0/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Filter out excluded attributes from each country object
    if excluded_attrs:
        filtered_data = []
        for country in data:
            filtered_country = {k: v for k, v in country.items() if k not in excluded_attrs}
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data