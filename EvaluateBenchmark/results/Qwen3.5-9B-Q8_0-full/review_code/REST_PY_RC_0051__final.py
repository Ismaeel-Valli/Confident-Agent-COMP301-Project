import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - included_attributes (list): Attributes to return for each country
            - search_text (str): Search term for filtering countries
            - credential (str): Caller-supplied authentication token
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
        Raises: Exception on unsuccessful HTTP response
    """
    base_url = "https://api.restcountries.com"
    
    params = {}
    
    # Add included attributes if provided
    if 'included_attributes' in inputs and inputs['included_attributes']:
        params['fields'] = ','.join(inputs['included_attributes'])
    
    # Add search text if provided
    if 'search_text' in inputs and inputs['search_text']:
        params['name'] = inputs['search_text']
    
    headers = {
        'Authorization': f'Bearer {inputs["credential"]}'
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data