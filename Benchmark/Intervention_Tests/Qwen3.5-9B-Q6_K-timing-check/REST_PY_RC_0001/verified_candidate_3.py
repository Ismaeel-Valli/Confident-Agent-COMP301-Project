import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 using the provided credential.
    
    Args:
        inputs (dict): Must contain 'credential' key with authentication token.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    credential = inputs["credential"]
    
    # REST Countries v5 uses bearer token authentication
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    url = "https://api.restcountries.com/v5/countries"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data