import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Currency code to match exactly
            - result_limit: Maximum number of results
            - results_to_skip: Number of results to skip
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "currency": value,
        "limit": result_limit,
        "skip": results_to_skip
    }
    
    # Make the request with the provided credential
    response = requests.get(base_url + "/v5.0/countries", params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data