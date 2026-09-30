import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: The calling code to match exactly
            - result_limit: Maximum number of results
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    calling_code = inputs["value"]
    result_limit = inputs["result_limit"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the query parameters
    params = {
        "fields": ",".join(included_attributes),
        "limit": str(result_limit)
    }
    
    # Make the GET request with credentials in headers
    response = requests.get(
        f"{base_url}/v5/calling-code/{calling_code}",
        params=params,
        headers={"Authorization": f"Bearer {credential}"}
    )
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data