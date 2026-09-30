import requests
import json

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 using the provided credential.
    
    Args:
        inputs (dict): Must contain 'credential' key with the API token.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    credential = inputs["credential"]
    url = "https://api.restcountries.com/v5/countries"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    return data