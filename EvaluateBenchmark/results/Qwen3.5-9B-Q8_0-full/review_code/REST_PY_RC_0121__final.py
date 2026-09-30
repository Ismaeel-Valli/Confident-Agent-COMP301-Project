import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: Currency code to match exactly
            - results_to_skip: Number of results to skip
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    value = inputs["value"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5/currency/{value}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    params = {
        "skip": results_to_skip
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    return response.json()