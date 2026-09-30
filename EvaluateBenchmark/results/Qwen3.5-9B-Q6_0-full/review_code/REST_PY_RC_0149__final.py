import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Capital city to match exactly
            - result_limit: Maximum number of results
            - included_attributes: List of country attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the API URL with query parameters
    base_url = "https://api.restcountries.com/v5.0/countries"
    params = {
        "capital": value,
        "limit": result_limit,
        "fields": ",".join(included_attributes)
    }
    
    # Make the request with the credential
    headers = {"Authorization": f"Bearer {credential}"}
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data