import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Three-letter ISO country code to match exactly
            - result_limit: Maximum number of results
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the API URL with query parameters for exact match
    base_url = "https://api.restcountries.com/v5.0/countries"
    params = {
        "iso": value,
        "limit": result_limit
    }
    
    # Make the request with the provided credential
    response = requests.get(base_url, params=params, headers={"Authorization": f"Bearer {credential}"})
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If the response is empty (no countries found), return None
    if not data:
        return None
    
    # Filter to only include requested attributes
    filtered_results = []
    for country in data:
        filtered_country = {}
        for attr in included_attributes:
            if attr in country:
                filtered_country[attr] = country[attr]
        filtered_results.append(filtered_country)
    
    return filtered_results