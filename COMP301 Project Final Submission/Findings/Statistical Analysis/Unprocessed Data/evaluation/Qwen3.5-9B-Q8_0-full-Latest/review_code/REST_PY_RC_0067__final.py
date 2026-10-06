import requests


def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Parameters:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip.
            - excluded_attributes (list): List of country attributes to exclude.
            - search_text (str): Search term for filtering countries.
            - credential (str): Caller-supplied credential (assumed valid).
    
    Returns:
        dict or None: Decoded JSON response if successful. Returns None for empty response.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://api.restcountries.com/v5/countries"
    params = {
        "page": 1,
        "results_to_skip": inputs["results_to_skip"],
        "excluded_attributes": ",".join(inputs["excluded_attributes"]),
        "search_text": inputs["search_text"],
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return None if len(data) == 0 else data
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")