import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5 API.
    
    Args:
        inputs (dict): Must contain:
            - value: Capital city name to match exactly
            - result_limit: Maximum number of results to return
            - included_attributes: List of country attributes to include in response
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    capital = inputs["value"]
    limit = inputs["result_limit"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for searching by capital
    base_url = "https://api.restcountries.com/v5.0/countries"
    
    # Build query parameters
    params = {
        "capital": capital,
        "limit": limit
    }
    
    # Make the request with credential in header
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If no results found, return None for successful empty response
    if not data or len(data) == 0:
        return None
    
    # Filter to only include requested attributes
    filtered_results = []
    for country in data:
        filtered_country = {}
        for attr in attributes:
            if attr in country:
                filtered_country[attr] = country[attr]
        filtered_results.append(filtered_country)
    
    return filtered_results