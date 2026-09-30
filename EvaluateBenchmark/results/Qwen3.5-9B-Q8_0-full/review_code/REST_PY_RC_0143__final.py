import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - "value": The capital city to match exactly
            - "credential": Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for filtering by capital
    url = "https://api.restcountries.com/v3.1/filter"
    params = {
        "capital": value,
        "fields": "*"  # Get all fields
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