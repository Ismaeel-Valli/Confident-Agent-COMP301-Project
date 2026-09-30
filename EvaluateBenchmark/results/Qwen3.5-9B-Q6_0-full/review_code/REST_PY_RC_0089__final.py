def solve(inputs):
    """
    Look up countries by exact region match using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: Region to match exactly
            - result_limit: Maximum number of results
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    base_url = "https://api.restcountries.com"
    region = inputs["value"]
    limit = inputs["result_limit"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5.0/countries?region={region}&limit={limit}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    # Filter to only included attributes
    filtered_data = []
    for country in data:
        filtered_country = {}
        for attr in attributes:
            if attr in country:
                filtered_country[attr] = country[attr]
        filtered_data.append(filtered_country)
    
    return filtered_data