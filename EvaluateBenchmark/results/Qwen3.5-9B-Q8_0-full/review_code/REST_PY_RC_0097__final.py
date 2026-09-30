import requests

def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - "value": The subregion to match exactly
            - "results_to_skip": Number of results to skip (for pagination)
            - "credential": Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    subregion = inputs["value"]
    skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # REST Countries v5 uses /v5.0/countries endpoint with query parameters
    params = {
        "subregion": subregion,
        "skip": skip
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(
        f"{base_url}/v5.0/countries",
        params=params,
        headers=headers
    )
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data