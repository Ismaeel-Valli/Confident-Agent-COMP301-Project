import requests
import json

def solve(inputs):
    """
    Search REST Countries v5 by search_text, returning only included_attributes.
    
    Args:
        inputs (dict): Must contain:
            - 'included_attributes': list of attribute names to return
            - 'search_text': string to search in country names
            - 'credential': API key for authentication
    
    Returns:
        dict or None: Decoded JSON response. None if successful but empty.
    
    Raises:
        Exception: If HTTP response is unsuccessful (non-2xx).
    """
    base_url = "https://api.restcountries.com"
    search_text = inputs["search_text"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5/search?name={search_text}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    # Filter to only include requested attributes
    filtered_data = []
    for country in data:
        filtered_country = {}
        for attr in included_attributes:
            if attr in country:
                filtered_country[attr] = country[attr]
        filtered_data.append(filtered_country)
    
    return filtered_data