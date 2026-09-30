import requests

def solve(inputs):
    """
    Search REST Countries v5 API with pagination and search.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip (pagination).
            - search_text (str): Search term for country names.
            - credential (str): Caller-supplied API token/credential.
    
    Returns:
        list or None: Decoded JSON response as a list, or None if empty but successful.
    
    Raises:
        Exception: For unsuccessful HTTP responses (non-2xx).
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/search/name"
    url = f"{base_url}{endpoint}"
    
    params = {
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"],
        "q": inputs["search_text"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (e.g., no results found)
    if not data:
        return None
    
    return data