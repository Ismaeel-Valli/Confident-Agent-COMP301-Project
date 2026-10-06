import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The capital city to match exactly
            - result_limit: Maximum number of results to return
            - excluded_attributes: List of country attributes to exclude from results
            - credential: Caller-supplied credential for authentication
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None if empty
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {
        "capital": inputs["value"],
        "limit": inputs["result_limit"]
    }
    
    # Make the API request with credential
    response = requests.get(
        f"{base_url}/v5/countries",
        params=params,
        headers={"Authorization": f"Bearer {inputs['credential']}"}
    )
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    # Filter out excluded attributes from each country object
    filtered_countries = []
    for country in data:
        filtered_country = {key: value for key, value in country.items() 
                          if key not in inputs["excluded_attributes"]}
        filtered_countries.append(filtered_country)
    
    return filtered_countries