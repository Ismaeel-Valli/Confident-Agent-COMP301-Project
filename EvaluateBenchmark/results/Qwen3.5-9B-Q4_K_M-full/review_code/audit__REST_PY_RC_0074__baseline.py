import requests

def solve(inputs):
    """
    Looks up countries by exact match on their common country name using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The exact country name to search for.
            - 'included_attributes': List of attributes to include in the response.
            - 'credential': Authentication token/credential for the API.
    
    Returns:
        dict or None: Decoded JSON response if found, None if successful but empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (non-2xx status code).
    """
    value = inputs.get('value')
    included_attributes = inputs.get('included_attributes', [])
    credential = inputs.get('credential')
    
    # Construct the API URL with query parameters
    url = "https://restcountries.com/v3.1/name"
    params = {
        'name': value,
        'fields': ','.join(included_attributes) if included_attributes else None
    }
    
    headers = {
        'Authorization': f'Bearer {credential}'
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    data = response.json()
    
    # Return None if the response is empty (successful but no results)
    if not data:
        return None
    
    return data