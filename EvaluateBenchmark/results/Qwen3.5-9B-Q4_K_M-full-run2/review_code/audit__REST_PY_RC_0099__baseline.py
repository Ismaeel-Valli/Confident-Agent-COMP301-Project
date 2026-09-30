import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their subregion using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The subregion value to match exactly.
            - 'excluded_attributes': List of attributes to exclude from the response.
            - 'credential': Caller-supplied credential (assumed to have necessary permissions).
    
    Returns:
        dict or None: Decoded JSON response if successful, or None for an empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    value = inputs['value']
    excluded_attributes = inputs.get('excluded_attributes', [])
    credential = inputs['credential']
    
    # Construct the API URL with query parameters
    base_url = "https://restcountries.com/v5.1"
    params = {
        'subregion': value,
        'fields': ','.join(excluded_attributes) if excluded_attributes else None
    }
    
    # Make the GET request
    response = requests.get(base_url, params=params, headers={'Authorization': f'Bearer {credential}'})
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None if the response is empty (successful but no results)
    if not data:
        return None
    
    return data