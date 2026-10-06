import requests

def solve(inputs):
    """
    Look up countries by exact currency code match from REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: Currency code to match exactly
            - result_limit: Maximum number of results
            - excluded_attributes: List of country attributes to exclude
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for filtering by currency code
    base_url = "https://api.restcountries.com/v5.0/countries"
    
    params = {
        "currency": value,
        "limit": result_limit
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter out excluded attributes from each country object
    filtered_countries = []
    for country in data:
        filtered_country = {}
        for key, val in country.items():
            if key not in excluded_attributes:
                filtered_country[key] = val
        filtered_countries.append(filtered_country)
    
    return filtered_countries