def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Parameters:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip (offset).
            - included_attributes (list): List of attributes to include in response.
            - search_text (str): Search term for country names.
            - credential (str): Caller-supplied credential (assumed valid).
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    base_url = "https://api.restcountries.com/v3.1/countries"
    params = {
        "skip": inputs["results_to_skip"],
        "search": inputs.get("search_text", ""),
        "_embed": ",".join(inputs.get("included_attributes", [])) if inputs.get("included_attributes") else None
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