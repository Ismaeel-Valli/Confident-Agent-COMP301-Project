import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return.
            - excluded_attributes (list): List of country attributes to exclude.
            - search_text (str): Search term for filtering countries.
            - credential (str): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v5/countries"
    params = {
        "limit": inputs["result_limit"],
        "searchText": inputs.get("search_text", ""),
        "excludeAttributes": ",".join(inputs.get("excluded_attributes", [])) if inputs.get("excluded_attributes") else None
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    return data