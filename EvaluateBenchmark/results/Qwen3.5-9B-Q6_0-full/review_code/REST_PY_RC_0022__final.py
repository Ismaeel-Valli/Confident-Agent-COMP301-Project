import requests

def solve(inputs):
    """
    Search country names in REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return
            - results_to_skip (int): Number of results to skip
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied authentication token
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/search/name"
    
    params = {
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"],
        "name": inputs["search_text"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    url = base_url + endpoint
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    if len(data) == 0:
        return None
    
    return data