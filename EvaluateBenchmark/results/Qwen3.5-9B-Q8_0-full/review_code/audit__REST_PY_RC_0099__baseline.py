import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their subregion using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The subregion value to match exactly.
            - 'excluded_attributes': List of attributes to exclude from the response.
            - 'credential': The caller-supplied credential (API key).
    
    Returns:
        dict or None: Decoded JSON response if successful, or None for an empty list.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    value = inputs['value']
    excluded_attributes = inputs.get('excluded_attributes', [])
    credential = inputs['credential']
    
    url = "https://restcountries.com/v3.1/subregion"
    params = {
        'subregion': value,
        'exclude': ','.join(excluded_attributes) if excluded_attributes else None
    }
    
    headers = {
        'Authorization': f'Bearer {credential}'
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data