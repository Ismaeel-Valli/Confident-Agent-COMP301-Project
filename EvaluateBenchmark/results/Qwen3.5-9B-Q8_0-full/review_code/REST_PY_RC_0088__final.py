import requests

def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The region to match exactly
            - result_limit: Maximum number of results
            - results_to_skip: Number of results to skip
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    region = inputs["value"]
    limit = inputs["result_limit"]
    skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5/region/{region}"
    
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
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data