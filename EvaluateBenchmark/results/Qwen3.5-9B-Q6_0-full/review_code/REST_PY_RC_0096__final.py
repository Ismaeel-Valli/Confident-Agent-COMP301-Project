import requests

def solve(inputs):
    """
    Look up countries by exact subregion match using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: Subregion to match exactly
            - result_limit: Maximum number of results
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    subregion = inputs["value"]
    limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    url = "https://api.restcountries.com/v5.0/countries"
    params = {
        "subregion": subregion,
        "limit": limit
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return data if data else None