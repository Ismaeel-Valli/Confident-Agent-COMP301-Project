import requests


def solve(inputs):
    """
    Look up countries by exact match on common name using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value (str): Country name to match exactly
            - results_to_skip (int): Number of results to skip
            - credential (str): Caller-supplied API key
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5.0/countries?name={inputs['value']}&skip={inputs['results_to_skip']}"
    
    headers = {
        "x-rcc-api-key": inputs["credential"]
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return None if len(data) == 0 else data
    
    raise Exception(f"HTTP {response.status_code}: {response.text}")