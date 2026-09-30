import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Parameters:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip (offset)
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied authentication token
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
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
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data