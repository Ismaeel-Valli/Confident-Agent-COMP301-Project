import requests

def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: The region to match exactly
            - result_limit: Maximum number of results
            - excluded_attributes: List of country attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    region = inputs["value"]
    limit = inputs["result_limit"]
    excluded_attrs = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "region": region,
        "limit": limit
    }
    
    # Make the request with credential in header
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(f"{base_url}/v5.0/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If empty response, return None
    if not data:
        return None
    
    # Filter out excluded attributes from each country object
    filtered_data = []
    for country in data:
        filtered_country = {}
        for key, value in country.items():
            if key not in excluded_attrs:
                filtered_country[key] = value
        filtered_data.append(filtered_country)
    
    return filtered_data