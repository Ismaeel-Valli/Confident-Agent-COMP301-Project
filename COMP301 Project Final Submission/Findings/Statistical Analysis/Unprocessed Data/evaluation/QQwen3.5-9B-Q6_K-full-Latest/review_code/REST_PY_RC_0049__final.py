def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Parameters:
        inputs (dict): Contains:
            - results_to_skip (int): Number of results to skip (offset)
            - search_text (str): Search term for country name
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5/countries"
    
    params = {
        "skip": inputs["results_to_skip"],
        "search": inputs["search_text"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    return data