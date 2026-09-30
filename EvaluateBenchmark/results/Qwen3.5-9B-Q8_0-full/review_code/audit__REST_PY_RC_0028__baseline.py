import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their two-letter ISO country code using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The two-letter ISO country code to match exactly.
            - 'result_limit': Maximum number of results to return.
            - 'included_attributes': List of attributes to include in the response.
            - 'credential': Caller-supplied credential (API key).
    
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty result.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    value = inputs['value']
    result_limit = inputs['result_limit']
    included_attributes = inputs['included_attributes']
    credential = inputs['credential']
    
    url = "https://restcountries.com/v3.1/alpha"
    params = {
        'code': value,
        'limit': result_limit,
        'fields': ','.join(included_attributes)
    }
    
    headers = {
        'Authorization': f'Bearer {credential}'
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data