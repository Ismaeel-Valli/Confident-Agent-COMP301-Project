import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Parameters:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip (offset).
            - included_attributes (list[str]): Attributes to include in response.
            - search_text (str): Search term for country names.
            - credential (str): Caller-supplied credential (assumed valid).
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://api.restcountries.com/v5"
    params = {
        "skip": inputs["results_to_skip"],
        "include": ",".join(inputs["included_attributes"]),
        "search": inputs["search_text"]
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return data if data else None
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")