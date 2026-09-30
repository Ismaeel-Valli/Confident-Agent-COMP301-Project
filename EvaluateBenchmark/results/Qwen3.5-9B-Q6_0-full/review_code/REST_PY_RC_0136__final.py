import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: The calling code to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - credential: Caller-supplied credential for authentication
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None if empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    calling_code = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Build the query parameters
    params = {
        "callingcode": calling_code,
        "limit": result_limit,
        "skip": results_to_skip
    }
    
    # Make the API request with the provided credential
    headers = {"Authorization": f"Bearer {credential}"}
    response = requests.get(f"{base_url}/v5.0/countries", params=params, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data