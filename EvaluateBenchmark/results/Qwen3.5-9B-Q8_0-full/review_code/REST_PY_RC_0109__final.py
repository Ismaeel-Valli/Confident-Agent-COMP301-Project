import requests

def solve(inputs):
    """
    Look up countries by an exact match on their bordering country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Country code to match exactly in borders list
            - results_to_skip (int): Number of results to skip
            - credential (str): Caller-supplied API key
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Get the country with the specified code to retrieve its borders
    url = f"{base_url}/v3.1/country/{value}"
    headers = {"X-Api-Key": credential}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    country_data = response.json()
    borders = country_data.get("borders", [])
    
    # Get all countries and filter by those that have the specified country in their borders
    url_all = f"{base_url}/v3.1/countries"
    response_all = requests.get(url_all, headers=headers)
    response_all.raise_for_status()
    
    if response_all.status_code == 204:
        return None
    
    all_countries = response_all.json()
    
    # Filter countries that have the specified country code in their borders list
    filtered_results = [country for country in all_countries if value in country.get("borders", [])]
    
    # Skip the requested number of results
    if len(filtered_results) > results_to_skip:
        return filtered_results[results_to_skip:]
    
    return filtered_results