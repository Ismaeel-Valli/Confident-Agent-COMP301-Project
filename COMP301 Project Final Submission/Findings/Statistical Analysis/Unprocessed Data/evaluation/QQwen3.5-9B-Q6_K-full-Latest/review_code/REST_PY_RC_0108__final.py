import requests

def solve(inputs):
    """
    Look up countries by an exact match on their bordering country code.
    
    Args:
        inputs (dict): Dictionary with keys:
            - value: Country code to match exactly (str)
            - result_limit: Maximum number of results (int)
            - credential: Caller-supplied credential (str)
    
    Returns:
        list or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    url = "https://api.restcountries.com/v3.1/alpha/borders"
    params = {
        "code": value,
        "limit": result_limit
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return data if data else None