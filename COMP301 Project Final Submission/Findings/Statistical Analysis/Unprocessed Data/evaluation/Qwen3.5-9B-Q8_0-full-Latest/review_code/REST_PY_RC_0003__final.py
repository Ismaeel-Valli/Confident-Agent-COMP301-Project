import requests

def solve(inputs):
    """
    Search REST Countries v5 by search_text using caller-supplied credential.
    
    Args:
        inputs (dict): Must contain 'search_text' and 'credential'.
        
    Returns:
        dict or None: Decoded JSON response, or None if empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    search_text = inputs["search_text"]
    credential = inputs["credential"]
    
    url = "https://api.restcountries.com/v5/search"
    params = {
        "q": search_text,
        "token": credential
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    data = response.json()
    return data