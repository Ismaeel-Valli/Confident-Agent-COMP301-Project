import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Contains:
            - value: Three-letter ISO country code to match exactly
            - result_limit: Maximum number of results
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    country_code = inputs["value"]
    limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5.2/country/{country_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (empty list or empty dict)
    if not data:
        return None
    
    return data