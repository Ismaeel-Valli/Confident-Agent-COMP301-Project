def solve(inputs):
    """
    Search REST Countries v5 using a provided credential.
    
    Args:
        inputs (dict): Must contain:
            - included_attributes (list[str]): Attributes to return.
            - search_text (str): Search term for country names.
            - credential (str): API key/credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response, or None if empty but successful.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    base_url = "https://api.restcountries.com/v5"
    url = f"{base_url}/search?name={inputs['search_text']}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    params = {}
    if inputs["included_attributes"]:
        params["fields"] = ",".join(inputs["included_attributes"])
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    return data