import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 using a caller-supplied credential.
    
    Args:
        inputs (dict): Must contain 'credential' key with the API token.
        
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    credential = inputs["credential"]
    
    # REST Countries v5 uses bearer token authentication
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    url = "https://api.restcountries.com/v5/countries"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data