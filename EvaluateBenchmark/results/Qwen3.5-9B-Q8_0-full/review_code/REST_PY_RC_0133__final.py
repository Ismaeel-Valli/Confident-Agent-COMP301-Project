import requests


def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The calling code to match exactly
            - results_to_skip: Number of results to skip
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    calling_code = inputs["value"]
    skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5/calling-code/{calling_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return None if len(data) == 0 else data
    elif response.status_code in (401, 403):
        raise Exception(f"Authentication failed: {response.status_code}")
    elif response.status_code in (404,):
        raise Exception(f"Resource not found: {response.status_code}")
    else:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")