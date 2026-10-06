import requests

def solve(inputs):
    """
    Look up countries by an exact match on their bordering country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Country code to match exactly in borders
            - result_limit (int): Maximum number of results
            - results_to_skip (int): Number of results to skip
            - credential (str): API key for authentication
    
    Returns:
        list or None: Decoded JSON response, or None if empty but successful
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5.0/countries?borders={value}&limit={result_limit}&skip={results_to_skip}"
    
    headers = {
        "x-rcc-api-key": credential,
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data