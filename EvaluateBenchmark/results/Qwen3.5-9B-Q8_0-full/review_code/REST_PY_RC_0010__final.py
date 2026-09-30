import requests

def solve(inputs):
    """
    Search country names in REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied authentication credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/search/name"
    url = f"{base_url}{endpoint}"
    
    params = {
        "search": inputs["search_text"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return None if len(data) == 0 else data
    
    raise Exception(f"HTTP {response.status_code}: {response.text}")