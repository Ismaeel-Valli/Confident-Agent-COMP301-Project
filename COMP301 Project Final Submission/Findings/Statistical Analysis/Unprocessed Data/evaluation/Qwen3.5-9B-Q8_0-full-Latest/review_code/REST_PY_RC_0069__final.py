import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Three-letter ISO country code to match exactly
            - result_limit (int): Maximum number of results to return
            - results_to_skip (int): Number of results to skip
            - included_attributes (list): List of attributes to include in the response
            - credential (str): Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    iso_code = inputs["value"]
    limit = inputs["result_limit"]
    skip = inputs["results_to_skip"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "iso3": iso_code,
        "limit": limit,
        "skip": skip,
        "fields": ",".join(attributes) if attributes else None
    }
    
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}
    
    # Make the request with credential
    headers = {"Authorization": f"Bearer {credential}"}
    
    response = requests.get(f"{base_url}/v5.1/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}, message: {response.text}")
    
    data = response.json()
    
    # If the response is an empty list, return None as per requirements
    if data == []:
        return None
    
    return data