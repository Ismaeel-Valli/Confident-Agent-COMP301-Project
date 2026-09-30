import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - 'value': The capital city to match exactly
            - 'results_to_skip': Number of results to skip
            - 'credential': Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    capital = inputs["value"]
    skip = inputs["results_to_skip"]
    
    url = f"{base_url}/v5/capital/{capital}"
    
    response = requests.get(url, headers={"Authorization": f"Bearer {inputs['credential']}"})
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # REST Countries v5 returns a list of countries matching the capital
    # We need to skip the first 'results_to_skip' results
    if isinstance(data, list):
        return data[skip:] if skip > 0 else data
    
    # If it's not a list (e.g., single result or error structure), return as-is
    return data