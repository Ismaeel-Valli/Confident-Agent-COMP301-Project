import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Country code to match exactly
            - result_limit: Maximum number of results
            - results_to_skip: Number of results to skip
            - credential: Caller-supplied authentication credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # REST Countries v5 uses /v5.1/countries/{code} endpoint
    url = f"{base_url}/v5.1/countries/{value}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    params = {}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return data if data else None