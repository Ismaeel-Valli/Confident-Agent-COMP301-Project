def solve(inputs):
    """
    Search REST Countries v5 using a provided credential.
    
    Args:
        inputs (dict): Must contain:
            - result_limit (int): Maximum number of results to return.
            - search_text (str): Search term for country names or codes.
            - credential (str): Caller-supplied API key/credential.
    
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx).
    """
    import requests
    
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/search"
    url = f"{base_url}{endpoint}"
    
    params = {
        "search": inputs["search_text"],
        "limit": inputs["result_limit"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return None if len(data) == 0 else data