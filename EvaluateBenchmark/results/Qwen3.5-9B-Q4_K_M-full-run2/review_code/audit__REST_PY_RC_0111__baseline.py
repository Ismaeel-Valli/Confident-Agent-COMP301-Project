import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their bordering country code using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The country code to match exactly for borders.
            - 'excluded_attributes': List of attributes to exclude from the response.
            - 'credential': Caller-supplied credential (e.g., API key or token).
    
    Returns:
        dict or None: Decoded JSON response, or None if the response is successfully empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    value = inputs.get("value")
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs.get("credential")
    
    # Base URL for REST Countries v5 API (using a public endpoint that supports filtering)
    # Note: The official REST Countries v5 API does not have a direct "bordering country code" filter in its standard GET /v3.1/countries endpoint.
    # However, we can fetch all countries and filter client-side for those that border the given country code.
    # Since the problem assumes referenced resources exist and we must use exact match on bordering country code,
    # we will construct a query to get countries where one of their borders matches the provided 'value'.
    
    # We'll use the /v3.1/countries endpoint which returns all countries with their borders.
    url = "https://restcountries.com/v3.1/all"
    
    headers = {}
    if credential:
        headers["Authorization"] = f"Bearer {credential}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses
    except requests.exceptions.RequestException as e:
        raise Exception(f"HTTP request failed: {e}")
    
    data = response.json()
    
    if not data:
        return None
    
    # Filter countries that have the given 'value' in their borders list
    matching_countries = []
    for country in data:
        borders = country.get("borders", [])
        if value in borders:
            # Exclude specified attributes
            filtered_country = {}
            for key, val in country.items():
                if key not in excluded_attributes:
                    filtered_country[key] = val
            matching_countries.append(filtered_country)
    
    return matching_countries