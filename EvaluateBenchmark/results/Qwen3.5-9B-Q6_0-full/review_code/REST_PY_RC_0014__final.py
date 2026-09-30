import requests

def solve(inputs):
    """
    Search country names using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_attributes (list): Attributes to include in response
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied authentication token
    
    Returns:
        dict or None: Decoded JSON response, or None if empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    api_url = "https://api.restcountries.com/v5.0/search"
    
    # Build query parameters
    params = {
        'search': inputs['search_text'],
        'fields': ','.join(inputs['included_attributes'])
    }
    
    # Make authenticated request
    headers = {
        'Authorization': f'Bearer {inputs["credential"]}'
    }
    
    response = requests.get(api_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data