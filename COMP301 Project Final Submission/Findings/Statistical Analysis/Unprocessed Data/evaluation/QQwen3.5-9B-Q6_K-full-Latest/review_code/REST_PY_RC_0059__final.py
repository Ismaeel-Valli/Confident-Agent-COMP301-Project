import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Parameters:
        inputs (dict): Must contain:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip (pagination).
            - search_text (str): Search term for filtering countries.
            - credential (str): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response if successful. Returns None for empty response.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
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
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data