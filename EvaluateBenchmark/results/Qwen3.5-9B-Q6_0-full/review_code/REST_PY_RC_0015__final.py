import requests

def solve(inputs):
    """
    Search REST Countries v5 by search_text, returning only included_attributes.
    
    Args:
        inputs (dict): Must contain:
            - credential (str): API key for authentication
            - search_text (str): Search term
            - included_attributes (list[str]): Attributes to include in response
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v5"
    search_text = inputs["search_text"]
    credential = inputs["credential"]
    included_attributes = inputs["included_attributes"]
    
    url = f"{base_url}/search?name={search_text}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    # Filter to only included attributes
    filtered_data = []
    for country in data:
        filtered_country = {}
        for attr in included_attributes:
            if attr in country:
                filtered_country[attr] = country[attr]
        filtered_data.append(filtered_country)
    
    return filtered_data