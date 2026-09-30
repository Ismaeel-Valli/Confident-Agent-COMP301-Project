import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Three-letter ISO country code to match exactly
            - result_limit (int): Maximum number of results to return
            - results_to_skip (int): Number of results to skip
            - credential (str): Caller-supplied API credential
    
    Returns:
        list or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v5"
    iso_code = inputs["value"]
    limit = inputs["result_limit"]
    skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    url = f"{base_url}/country/{iso_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    params = {
        "limit": limit,
        "skip": skip
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data