import requests


def solve(inputs):
    """
    Look up countries by exact match on their common country name using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Country name to match exactly
            - result_limit (int): Maximum number of results
            - included_attributes (list): Attributes to return for each country
            - credential (str): Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response. None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v5/countries"
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "name": value,
        "limit": result_limit,
        "fields": ",".join(included_attributes)
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # REST Countries v5 returns empty list for no matches, not null
    return data if data else None