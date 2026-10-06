import requests

def solve(inputs):
    """
    Look up countries by an exact match on their two-letter ISO country code using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The two-letter ISO country code to match exactly.
            - 'result_limit': Maximum number of results to return.
            - 'included_attributes': List of attributes to include in the response.
            - 'credential': Caller-supplied credential (e.g., API key or token).
    
    Returns:
        dict or None: Decoded JSON response if successful, or None for an empty result set.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    value = inputs['value']
    result_limit = inputs['result_limit']
    included_attributes = inputs['included_attributes']
    credential = inputs['credential']
    
    # Construct the API URL with query parameters
    url = "https://restcountries.com/v3.1/alpha"
    params = {
        'code': value,
        'limit': result_limit,
        'fields': ','.join(included_attributes)
    }
    
    headers = {
        'Authorization': f'Bearer {credential}' if credential.startswith('Bearer ') else f'{credential}',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # If the response is an empty list (no countries found), return None
        if isinstance(data, list) and len(data) == 0:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")