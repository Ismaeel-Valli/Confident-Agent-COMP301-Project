import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Parameters:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip (for pagination).
            - search_text (str): Search term for filtering countries.
            - credential (str): Caller-supplied credential (assumed valid).
    
    Returns:
        list or None: Decoded JSON response as a list of country objects, 
                      or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (non-2xx status code).
    """
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5/countries"
    
    params = {
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"],
        "search": inputs["search_text"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data