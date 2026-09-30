import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The calling code to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to include in the response
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    calling_code = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the query parameters
    params = {
        "callingCode": calling_code,
        "limit": result_limit,
        "skip": results_to_skip
    }
    
    # If included_attributes is provided, add it to params
    if included_attributes:
        params["fields"] = ",".join(included_attributes)
    
    # Make the API request with the credential in headers
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(f"{base_url}/v5/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data