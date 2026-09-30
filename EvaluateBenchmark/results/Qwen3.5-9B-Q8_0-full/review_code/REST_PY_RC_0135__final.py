import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code from REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: The calling code to match exactly
            - excluded_attributes: List of country attributes to exclude from results
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty response
        Raises: Exception for unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    calling_code = inputs["value"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    url = f"{base_url}/v5/calling-code/{calling_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If the response is empty (e.g., no countries found), return None
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