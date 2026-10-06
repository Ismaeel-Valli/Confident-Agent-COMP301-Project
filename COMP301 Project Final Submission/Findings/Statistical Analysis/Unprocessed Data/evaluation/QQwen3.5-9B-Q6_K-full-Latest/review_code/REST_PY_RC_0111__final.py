import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Country code to match exactly in borders
            - excluded_attributes: List of attributes to exclude from results
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # Use REST Countries v5 API - get all countries and filter by borders
    url = "https://api.restcountries.com/v3.1/countries"
    params = {
        "code": value,
        "credential": credential
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If no country found (empty response), return None
    if not data:
        return None
    
    # Get the borders of the target country
    border_codes = data.get("borders", [])
    
    # Find all countries that have this country in their borders list
    results = []
    for code in border_codes:
        url_country = f"https://api.restcountries.com/v3.1/countries/{code}"
        params_country = {
            "credential": credential
        }
        
        response_country = requests.get(url_country, params=params_country)
        
        if response_country.status_code == 200:
            country_data = response_country.json()
            # Check if the target country is in this country's borders
            if value in country_data.get("borders", []):
                results.append(country_data)
    
    # If no countries found (empty response), return None
    if not results:
        return None
    
    # Filter out excluded attributes if any
    if excluded_attributes:
        filtered_results = []
        for country in results:
            filtered_country = {k: v for k, v in country.items() if k not in excluded_attributes}
            filtered_results.append(filtered_country)
        return filtered_results
    
    return results