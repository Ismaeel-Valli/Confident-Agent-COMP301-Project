import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Three-letter ISO country code to match exactly
            - result_limit: Maximum number of results
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    iso_code = inputs["value"]
    limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v3.0/countries?iso3={iso_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return None if not data else data
    elif response.status_code == 404:
        raise Exception(f"Country with ISO code '{iso_code}' not found")
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")