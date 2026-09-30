import requests
import json

def solve(inputs):
    """
    Search REST Countries v5 by search term using caller-supplied credential.
    
    Args:
        inputs (dict): Must contain 'search_text' and 'credential'.
        
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    search_text = inputs["search_text"]
    credential = inputs["credential"]
    
    base_url = "https://api.restcountries.com/v5"
    url = f"{base_url}/search?name={search_text}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return None if len(data) == 0 else data
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")