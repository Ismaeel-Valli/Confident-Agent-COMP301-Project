import requests

def solve(inputs):
    """
    Search countries on REST Countries v5 API using provided inputs.
    
    Parameters:
        inputs (dict): Must contain:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip.
            - included_attributes (list[str]): Attributes to include in response.
            - search_text (str): Search term for country names.
            - credential (str): Caller-supplied authentication token.
    
    Returns:
        dict or None: Decoded JSON response if successful. Returns None for empty results.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/search"
    
    params = {
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"],
        "fields": ",".join(inputs["included_attributes"]),
        "q": inputs["search_text"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    url = base_url + endpoint
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            return None if len(data) == 0 else data
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")