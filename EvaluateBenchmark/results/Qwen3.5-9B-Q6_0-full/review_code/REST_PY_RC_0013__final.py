import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_attributes (list): Attributes to include in response
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    api_url = "https://api.restcountries.com/v5/countries"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    params = {}
    if 'included_attributes' in inputs and inputs['included_attributes']:
        params['fields'] = ','.join(inputs['included_attributes'])
    
    response = requests.get(api_url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data