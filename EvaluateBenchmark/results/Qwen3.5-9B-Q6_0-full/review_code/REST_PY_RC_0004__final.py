import requests

def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code.
    
    Args:
        inputs (dict): Must contain:
            - "value": str, the two-letter ISO country code to match exactly
            - "credential": str, caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    value = inputs["value"]
    credential = inputs["credential"]
    
    # Use the REST Countries API endpoint for country lookup by ISO code
    url = "https://api.restcountries.com/v3.1/all"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    params = {
        "iso2": value
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (no countries found)
    if not data:
        return None
    
    return data