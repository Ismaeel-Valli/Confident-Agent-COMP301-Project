import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5, excluding specified attributes.
    
    Args:
        inputs (dict): Must contain:
            - 'excluded_attributes': list of attribute names to exclude
            - 'credential': caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response. None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    excluded_attributes = inputs.get('excluded_attributes', [])
    credential = inputs.get('credential')
    
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5/countries?page=1&per_page=100"
    
    headers = {
        'Authorization': f'Bearer {credential}'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
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
    
    return {
        'data': filtered_countries,
        'page': 1,
        'per_page': 100
    }