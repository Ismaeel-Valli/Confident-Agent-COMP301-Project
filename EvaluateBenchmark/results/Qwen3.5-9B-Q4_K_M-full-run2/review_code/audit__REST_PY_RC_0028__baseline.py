import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their two-letter ISO country code using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The two-letter ISO country code to match exactly.
            - 'result_limit': Maximum number of results to return.
            - 'included_attributes': List of attributes to include in the response.
            - 'credential': Caller-supplied credential (e.g., API key or token).
    
    Returns:
        list|None: Decoded JSON response as a list of country objects, or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status code).
    """
    value = inputs.get('value')
    result_limit = inputs.get('result_limit', 10)
    included_attributes = inputs.get('included_attributes', [])
    credential = inputs.get('credential')
    
    # Construct the query string parameters
    params = {
        'q': value,
        'limit': result_limit,
        'fields': ','.join(included_attributes) if included_attributes else None
    }
    
    # Remove None fields from params to avoid sending empty values
    params = {k: v for k, v in params.items() if v is not None}
    
    url = "https://restcountries.com/v3.1"
    
    headers = {}
    if credential:
        headers['Authorization'] = f'Bearer {credential}'
    
    response = requests.get(url, params=params, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses (non-2xx status codes)
    response.raise_for_status()
    
    data = response.json()
    
    # Return None if the response is empty (successful but no results)
    if not data:
        return None
    
    return data