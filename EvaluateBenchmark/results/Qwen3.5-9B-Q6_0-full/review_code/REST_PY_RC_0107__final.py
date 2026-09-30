import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - "value": The country code to match exactly
            - "credential": Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    credential = inputs["credential"]
    
    # API endpoint for REST Countries v5 - lookup by bordering country code
    url = "https://api.restcountries.com/v3.1/all"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    params = {
        "borders": value
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (no borders found)
    if not data or len(data) == 0:
        return None
    
    return data