import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5, excluding specified attributes.
    
    Args:
        inputs (dict): Must contain:
            - 'excluded_attributes': list of attribute names to exclude
            - 'credential': caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    excluded_attributes = inputs.get('excluded_attributes', [])
    credential = inputs['credential']
    
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5/countries?page=1&fields=-{','.join(excluded_attributes)}"
    
    headers = {
        'Authorization': f'Bearer {credential}'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return None if len(data) == 0 else data
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")