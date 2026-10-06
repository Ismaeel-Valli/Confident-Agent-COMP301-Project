import requests

def solve(inputs):
    """
    Search REST Countries v5 using provided inputs.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results
            - excluded_attributes (list): Attributes to exclude
            - search_text (str): Search term
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {
        "search": inputs["search_text"],
        "limit": inputs["result_limit"]
    }
    
    # Make the request with credential in header
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(f"{base_url}/v5/search", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If empty response, return None as per spec
    if not data:
        return None
    
    # Filter out excluded attributes from each country object
    filtered_countries = []
    for country in data:
        filtered_country = {}
        for key, value in country.items():
            if key not in inputs["excluded_attributes"]:
                filtered_country[key] = value
        filtered_countries.append(filtered_country)
    
    return filtered_countries