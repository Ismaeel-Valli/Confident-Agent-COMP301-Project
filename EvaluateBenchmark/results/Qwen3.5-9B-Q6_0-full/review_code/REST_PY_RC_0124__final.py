import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: Currency code to match exactly
            - result_limit: Maximum number of results
            - results_to_skip: Number of results to skip
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    currency_code = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "currency": currency_code,
        "limit": result_limit,
        "skip": results_to_skip
    }
    
    # Make the request with credentials in header
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(base_url + "/v5.0/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    return response.json()