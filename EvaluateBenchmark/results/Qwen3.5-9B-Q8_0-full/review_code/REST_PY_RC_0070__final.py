import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Three-letter ISO country code to match exactly
            - result_limit (int): Maximum number of results to return
            - results_to_skip (int): Number of results to skip
            - excluded_attributes (list): List of country attributes to exclude from response
            - credential (str): Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    iso_code = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters - REST Countries v5 uses /v5/all endpoint with filter params
    params = {
        "iso3": iso_code,
        "limit": result_limit,
        "skip": results_to_skip,
        "excludes": ",".join(excluded_attributes) if excluded_attributes else ""
    }
    
    # Make the request with credential in header
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(f"{base_url}/v5/all", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # REST Countries v5 returns an array of countries
    return data if data else None