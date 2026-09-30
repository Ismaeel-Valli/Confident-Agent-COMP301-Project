import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Currency code to match exactly
            - result_limit: Maximum number of results
            - excluded_attributes: List of country attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for filtering by currency
    base_url = "https://api.restcountries.com/v5.0"
    url = f"{base_url}/currency/{value}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    params = {
        "limit": result_limit
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If empty response, return None as per spec
    if not data:
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