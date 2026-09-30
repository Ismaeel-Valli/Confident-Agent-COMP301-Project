import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - "value": The currency code to match exactly
            - "credential": Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    credential = inputs["credential"]
    
    # REST Countries v5 endpoint for filtering by currency code
    url = "https://api.restcountries.com/v3.1/filter"
    params = {
        "currency": value,
        "fields": "name,cca2,ccn,flag,currencies"
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (no countries found)
    if not data:
        return None
    
    return data