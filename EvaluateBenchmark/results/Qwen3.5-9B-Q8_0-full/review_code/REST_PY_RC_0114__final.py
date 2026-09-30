import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Country code to match exactly in borders
            - result_limit: Maximum number of results to return
            - excluded_attributes: List of attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "border": value,
        "limit": result_limit
    }
    
    # Make the API request with credentials in header
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
        for key, val in country.items():
            if key not in excluded_attributes:
                filtered_country[key] = val
        filtered_data.append(filtered_country)
    
    return filtered_data