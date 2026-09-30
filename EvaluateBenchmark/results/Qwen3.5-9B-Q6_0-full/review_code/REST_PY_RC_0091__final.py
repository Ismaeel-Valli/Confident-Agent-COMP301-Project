import requests

def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The region to match exactly
            - results_to_skip: Number of results to skip (for pagination)
            - included_attributes: List of attributes to return for each country
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
        Raises: Exception for unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    region = inputs["value"]
    skip = inputs["results_to_skip"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5.1/countries?region={region}&skip={skip}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    # Filter to only include requested attributes
    filtered_data = []
    for country in data:
        filtered_country = {}
        for attr in attributes:
            if attr in country:
                filtered_country[attr] = country[attr]
        filtered_data.append(filtered_country)
    
    return filtered_data