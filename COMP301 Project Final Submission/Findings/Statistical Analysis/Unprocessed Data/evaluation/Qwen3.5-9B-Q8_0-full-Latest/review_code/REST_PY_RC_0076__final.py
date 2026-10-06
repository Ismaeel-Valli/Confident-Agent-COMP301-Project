import requests

def solve(inputs):
    """
    Look up countries by exact match on their common country name using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): The exact country name to match
            - result_limit (int): Maximum number of results to return
            - results_to_skip (int): Number of results to skip
            - credential (str): Caller-supplied API key
    
    Returns:
        list or None: Decoded JSON response as a list, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5.0/countries?name={value}&limit={result_limit}&skip={results_to_skip}"
    
    headers = {
        "x-rcc-api-key": credential,
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return data if data else None
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")