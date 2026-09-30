import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - "value": The three-letter ISO country code to match exactly
            - "credential": Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    iso_code = inputs["value"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5.0/country/{iso_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return None if not data else data
    elif response.status_code == 404:
        raise Exception(f"Country with ISO code '{iso_code}' not found")
    else:
        raise Exception(f"HTTP error {response.status_code}: {response.text}")