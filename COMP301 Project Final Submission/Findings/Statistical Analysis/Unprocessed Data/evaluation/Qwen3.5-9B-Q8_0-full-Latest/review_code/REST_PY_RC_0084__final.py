import requests

def solve(inputs):
    """
    Look up countries by exact region match using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Region name to match exactly
            - result_limit: Maximum number of results to return
            - credential: Caller-supplied authentication credential
    
    Returns:
        list or None: Decoded JSON response as a list, or None for empty successful response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    base_url = "https://api.restcountries.com"
    endpoint = f"/v5/region/{value}"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    params = {
        "limit": result_limit
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data