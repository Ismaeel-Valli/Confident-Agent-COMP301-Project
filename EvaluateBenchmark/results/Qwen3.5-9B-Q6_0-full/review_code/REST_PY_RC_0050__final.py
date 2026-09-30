import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Must contain:
            - "value": str, the three-letter ISO country code to match exactly
            - "credential": str, caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    iso_code = inputs["value"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5/country/{iso_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return None if len(data) == 0 else data
    elif response.status_code == 404:
        raise Exception(f"Country not found for ISO code: {iso_code}")
    else:
        raise Exception(f"HTTP error {response.status_code}: {response.text}")