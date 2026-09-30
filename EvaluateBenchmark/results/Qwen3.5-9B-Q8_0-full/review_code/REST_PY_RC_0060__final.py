import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Three-letter ISO country code to match exactly
            - result_limit (int): Maximum number of results
            - results_to_skip (int): Number of results to skip
            - credential (str): Caller-supplied API credential
    
    Returns:
        list or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    iso_code = inputs["value"]
    limit = inputs["result_limit"]
    skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5.0/countries/{iso_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    params = {
        "limit": limit,
        "skip": skip
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (empty list)
    if not data:
        return None
    
    return data