def solve(inputs):
    """
    Search REST Countries v5 using a caller-supplied credential.
    
    Args:
        inputs (dict): Must contain:
            - results_to_skip (int): Number of results to skip.
            - search_text (str): Search term.
            - credential (str): Caller-supplied API key/credential.
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/search"
    url = f"{base_url}{endpoint}"
    
    params = {
        "search": inputs["search_text"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return None if len(data) == 0 else data
    
    raise Exception(f"HTTP {response.status_code}: {response.text}")