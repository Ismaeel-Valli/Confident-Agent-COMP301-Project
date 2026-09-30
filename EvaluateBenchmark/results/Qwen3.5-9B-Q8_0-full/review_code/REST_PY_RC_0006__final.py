import requests

def solve(inputs):
    """
    Search country names in REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied authentication credential
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/search/name"
    
    url = f"{base_url}{endpoint}"
    
    params = {
        "search": inputs["search_text"],
        "limit": inputs["result_limit"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data