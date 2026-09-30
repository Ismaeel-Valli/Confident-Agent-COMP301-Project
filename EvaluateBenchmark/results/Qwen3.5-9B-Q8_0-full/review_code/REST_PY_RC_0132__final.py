import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The calling code to match exactly
            - result_limit: Maximum number of results
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    calling_code = inputs["value"]
    result_limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5/calling-code/{calling_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (empty list)
    if isinstance(data, list) and len(data) == 0:
        return None
    
    return data