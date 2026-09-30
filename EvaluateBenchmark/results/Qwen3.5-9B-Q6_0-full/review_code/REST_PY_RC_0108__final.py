import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Country code to match exactly
            - result_limit (int): Maximum number of results
            - credential (str): Caller-supplied API key
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    url = "https://api.restcountries.com/v3.1/all"
    
    headers = {
        "x-api-key": credential
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    return response.json()