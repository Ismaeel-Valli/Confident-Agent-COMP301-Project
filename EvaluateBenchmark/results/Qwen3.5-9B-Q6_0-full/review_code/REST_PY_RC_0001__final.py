import requests


def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 using the provided credential.
    
    Parameters:
        inputs (dict): Must contain 'credential' key with the API key.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    api_key = inputs["credential"]
    url = "https://api.restcountries.com/v5/countries"
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return data if data else None
    
    raise Exception(f"HTTP error: {response.status_code}")