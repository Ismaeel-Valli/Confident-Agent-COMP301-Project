import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their common country name using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The exact country name to search for.
            - 'included_attributes': List of attributes to include in the response.
            - 'credential': API key/credential for authentication.
    
    Returns:
        dict or None: Decoded JSON response if found, or None if no countries match.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not 200).
    """
    value = inputs['value']
    included_attributes = inputs.get('included_attributes', [])
    credential = inputs['credential']
    
    # Construct the query parameters
    params = {
        'name': value,
        'fields': ','.join(included_attributes) if included_attributes else None
    }
    
    url = "https://restcountries.com/v3.1/name"
    
    headers = {
        'Authorization': f'Bearer {credential}'
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code: {response.status_code}")
    
    data = response.json()
    
    # If the response is a list and empty, return None
    if isinstance(data, list) and len(data) == 0:
        return None
    
    return data