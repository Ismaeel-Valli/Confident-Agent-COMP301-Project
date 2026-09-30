import requests


def solve(inputs):
    """
    Look up countries by exact currency code match using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value (str): Currency code to match exactly
            - result_limit (int): Maximum number of results
            - credential (str): Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    currency_code = inputs["value"]
    limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    url = f"{base_url}/currency/{currency_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    params = {
        "limit": limit
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data