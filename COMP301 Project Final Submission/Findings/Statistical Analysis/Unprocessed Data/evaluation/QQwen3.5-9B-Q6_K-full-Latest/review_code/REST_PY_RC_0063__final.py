import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return
            - excluded_attributes (list): Attributes to exclude from response
            - search_text (str): Search term for filtering countries
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5"
    
    # Build query parameters
    params = {
        'limit': inputs['result_limit'],
        'search': inputs.get('search_text', ''),
        'credential': inputs['credential']
    }
    
    # Make the request
    response = requests.get(base_url, params=params)
    
    # Check for unsuccessful HTTP response
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    # Exclude specified attributes from each country object
    excluded_attrs = inputs.get('excluded_attributes', [])
    filtered_data = []
    
    for country in data:
        filtered_country = {k: v for k, v in country.items() if k not in excluded_attrs}
        filtered_data.append(filtered_country)
    
    return filtered_data