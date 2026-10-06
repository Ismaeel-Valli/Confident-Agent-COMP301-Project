import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_attributes (list): Attributes to include in response
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    api_url = "https://api.restcountries.com/v5/countries"
    
    params = {
        "page": 1,
        "pageSize": 10,
        "searchText": inputs.get("search_text", ""),
        "fields": ",".join(inputs.get("included_attributes", [])) if inputs.get("included_attributes") else None
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(api_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return None if not data else data