import requests

def solve(inputs):
    """
    Look up countries by exact subregion match using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Subregion to match exactly
            - results_to_skip: Number of results to skip (offset)
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    subregion = inputs["value"]
    skip = inputs["results_to_skip"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "subregion": subregion,
        "skip": skip,
        "fields": ",".join(attributes)
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(f"{base_url}/v5/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # REST Countries v5 returns an array of countries
    if len(data) == 0:
        return None
    
    return data