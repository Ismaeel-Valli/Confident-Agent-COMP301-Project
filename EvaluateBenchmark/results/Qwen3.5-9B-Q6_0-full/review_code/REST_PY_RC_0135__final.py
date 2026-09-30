import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code from REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The calling code to match exactly
            - excluded_attributes: List of country attributes to exclude from results
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    calling_code = inputs["value"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for searching by calling code
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5.1/calling-code/{calling_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If the response is an empty list or indicates no results, return None
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