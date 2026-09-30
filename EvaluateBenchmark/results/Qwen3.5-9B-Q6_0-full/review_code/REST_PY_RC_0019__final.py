import requests

def solve(inputs):
    """
    Search REST Countries v5 by search_text, excluding specified attributes.
    
    Args:
        inputs (dict): Contains:
            - excluded_attributes (list): Attributes to exclude from response
            - search_text (str): Search term for country names
            - credential (str): API key/credential
    
    Returns:
        dict or None: Decoded JSON response, or None if empty successful response
    """
    base_url = "https://api.restcountries.com/v5"
    
    # Build query parameters
    params = {
        'search': inputs['search_text'],
        'exclude': ','.join(inputs['excluded_attributes'])
    }
    
    # Make the request with provided credential
    response = requests.get(
        f"{base_url}/countries",
        params=params,
        headers={'Authorization': f'Bearer {inputs["credential"]}'}
    )
    
    # Raise exception for unsuccessful HTTP response
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data