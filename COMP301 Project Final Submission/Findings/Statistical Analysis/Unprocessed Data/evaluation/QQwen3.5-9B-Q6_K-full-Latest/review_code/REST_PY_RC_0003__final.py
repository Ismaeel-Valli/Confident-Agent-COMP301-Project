import requests

def solve(inputs):
    """
    Search REST Countries v5 using a search term.
    
    Args:
        inputs (dict): Must contain 'search_text' and 'credential'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v5"
    search_term = inputs["search_text"]
    credential = inputs["credential"]
    
    url = f"{base_url}/search?name={search_term}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    return data