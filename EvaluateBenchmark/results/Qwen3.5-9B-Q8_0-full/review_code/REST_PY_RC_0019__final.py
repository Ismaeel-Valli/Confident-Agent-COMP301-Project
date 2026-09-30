import requests
import json

def solve(inputs):
    """
    Search REST Countries v5 by search_text, excluding specified attributes.
    
    Args:
        inputs (dict): Must contain:
            - excluded_attributes (list): Attributes to exclude from results
            - search_text (str): Search term for country names
            - credential (str): API key/credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    search_text = inputs["search_text"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "name": search_text,
        "exclude": ",".join(excluded_attributes) if excluded_attributes else None
    }
    
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(f"{base_url}/v5/search", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data