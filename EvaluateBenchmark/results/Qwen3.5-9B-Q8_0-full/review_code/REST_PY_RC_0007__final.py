import requests

def solve(inputs):
    """
    Search REST Countries v5 by country name or code.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - search_text (str): Search term for country name or code.
            - credential (str): Caller-supplied API credential.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/search/country"
    
    params = {
        "search": inputs["search_text"],
        "limit": inputs["result_limit"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    url = base_url + endpoint
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data