import requests

def solve(inputs):
    """
    Look up countries by exact match on their common country name using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The country name to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - credential: Caller-supplied authentication credential
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build the query parameters
    params = {
        "name": inputs["value"],
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    # Make the GET request with credentials in header
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(f"{base_url}/v5/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    return response.json()