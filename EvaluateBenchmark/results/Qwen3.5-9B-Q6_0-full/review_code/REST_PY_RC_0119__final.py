import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5 API.
    
    Args:
        inputs (dict): Must contain:
            - "value": The currency code to match exactly
            - "credential": Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses (non-2xx status codes).
    """
    value = inputs["value"]
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for filtering by currency code
    url = "https://api.restcountries.com/v3.1/filter"
    params = {
        "currencies": value,
        "fields": "name,cca2,ccn3,currencies"
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data