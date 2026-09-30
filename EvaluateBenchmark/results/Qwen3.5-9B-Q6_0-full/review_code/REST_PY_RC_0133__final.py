import requests


def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5.
    
    Args:
        inputs (dict): Must contain:
            - "value": str, the calling code to match exactly
            - "results_to_skip": int, number of results to skip
            - "credential": str, caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    calling_code = inputs["value"]
    skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5/calling-code/{calling_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    if isinstance(data, list):
        return None if len(data) == 0 else data
    
    return data