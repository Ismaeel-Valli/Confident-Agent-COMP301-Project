import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code from REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: The calling code to match exactly
            - result_limit: Maximum number of results
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of attributes to exclude from each country
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
    
    # Build query parameters
    params = {
        "callingcode": calling_code,
        "limit": result_limit,
        "skip": results_to_skip
    }
    
    # Make the API request with the provided credential
    headers = {"Authorization": f"Bearer {credential}"}
    response = requests.get(f"{base_url}/v5.0/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If the response is empty (successful but no results), return None
    if not data:
        return None
    
    # Filter out excluded attributes from each country object
    filtered_countries = []
    for country in data:
        filtered_country = {key: value for key, value in country.items() 
                          if key not in excluded_attributes}
        filtered_countries.append(filtered_country)
    
    return filtered_countries