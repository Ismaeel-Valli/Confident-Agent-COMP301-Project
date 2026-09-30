import requests

def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Region to match exactly
            - result_limit: Maximum number of results
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    api_url = "https://api.restcountries.com/v5.0/countries"
    
    params = {
        "region": inputs["value"],
        "limit": inputs["result_limit"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(api_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return data if data else None