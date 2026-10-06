def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Region to match exactly
            - results_to_skip (int): Number of results to skip (pagination)
            - included_attributes (list[str]): Attributes to return for each country
            - credential (str): Caller-supplied API key
    
    Returns:
        dict or None: Decoded JSON response. None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    base_url = "https://api.restcountries.com/v5"
    region = inputs["value"]
    skip = inputs["results_to_skip"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    url = f"{base_url}/region/{region}?skip={skip}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter to only included attributes
    filtered_data = []
    for country in data:
        filtered_country = {}
        for attr in attributes:
            if attr in country:
                filtered_country[attr] = country[attr]
        filtered_data.append(filtered_country)
    
    return filtered_data if filtered_data else None