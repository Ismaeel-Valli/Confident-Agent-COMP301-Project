import requests

def solve(inputs):
    """
    Search country names on REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - included_attributes (list): Attributes to return
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    search_text = inputs["search_text"]
    credential = inputs["credential"]
    included_attributes = inputs["included_attributes"]
    
    # Build query parameters
    params = {
        "name": search_text,
        "fields": ",".join(included_attributes)
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(base_url + "/v5", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data