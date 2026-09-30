def solve(inputs):
    """
    Search country names using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return
            - excluded_attributes (list): Attributes to exclude from results
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied API key
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    base_url = "https://api.restcountries.com/v5"
    search_text = inputs["search_text"]
    result_limit = inputs["result_limit"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters - REST Countries v5 uses different endpoint structure
    params = {
        "name": search_text,
        "limit": result_limit
    }
    
    # Make the API request with credentials in header
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(f"{base_url}/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If successful but empty, return None
    if not data:
        return None
    
    # Filter out excluded attributes from each country object
    filtered_data = []
    for country in data:
        filtered_country = {}
        for key, value in country.items():
            if key not in excluded_attributes:
                filtered_country[key] = value
        filtered_data.append(filtered_country)
    
    return filtered_data