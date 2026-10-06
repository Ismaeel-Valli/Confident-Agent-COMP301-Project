import requests

def solve(inputs):
    """
    Search REST Countries v5 by text, excluding specified attributes.
    
    Args:
        inputs (dict): Must contain:
            - excluded_attributes (list): Attributes to exclude from results
            - search_text (str): Search term for country names
            - credential (str): API key/credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    api_key = inputs["credential"]
    search_text = inputs["search_text"]
    excluded_attributes = inputs["excluded_attributes"]
    
    base_url = "https://api.restcountries.com/v5.0"
    url = f"{base_url}/search?name={search_text}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }
    
    params = {
        "name": search_text,
        "exclude": ",".join(excluded_attributes) if excluded_attributes else ""
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return None if not data else data