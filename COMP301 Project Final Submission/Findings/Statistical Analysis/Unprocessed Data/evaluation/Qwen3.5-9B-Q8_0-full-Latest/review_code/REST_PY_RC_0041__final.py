import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip
            - included_attributes (list): Attributes to include in response
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {
        'page': 1,
        'skip': inputs['results_to_skip'],
        'fields': ','.join(inputs['included_attributes'])
    }
    
    # Make the request with credential in headers
    response = requests.get(
        base_url + '/countries/v5',
        params=params,
        headers={'Authorization': f'Bearer {inputs["credential"]}'}
    )
    
    # Check for unsuccessful HTTP response
    if not response.ok:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for empty successful response
    if len(data) == 0:
        return None
    
    return data