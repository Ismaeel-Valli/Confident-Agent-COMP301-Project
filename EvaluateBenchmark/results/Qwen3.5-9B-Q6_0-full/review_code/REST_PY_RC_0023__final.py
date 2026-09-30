import requests

def solve(inputs):
    """
    Search REST Countries v5 using provided inputs.
    
    Args:
        inputs (dict): Must contain:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip (pagination).
            - search_text (str): Search term for country names.
            - credential (str): Caller-supplied API key/credential.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/search"
    
    params = {
        "search": inputs["search_text"],
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
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