import requests

def solve(inputs):
    """
    Search REST Countries v5 using a provided credential.
    
    Args:
        inputs (dict): Must contain:
            - results_to_skip (int): Number of results to skip (pagination offset)
            - search_text (str): Search term for country names
            - credential (str): API key/credential
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty responses.
    
    Raises:
        Exception: For unsuccessful HTTP responses (non-2xx status codes).
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/search/name"
    url = f"{base_url}{endpoint}"
    
    params = {
        "search": inputs["search_text"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "x-api-key": inputs["credential"]
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty responses (empty list)
    if data is None or len(data) == 0:
        return None
    
    return data