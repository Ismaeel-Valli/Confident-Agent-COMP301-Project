import requests

def solve(inputs):
    """
    Look up countries by exact match on subregion using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: Subregion to match exactly
            - results_to_skip: Number of results to skip (offset)
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    subregion = inputs["value"]
    skip = inputs["results_to_skip"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "subregion": subregion,
        "skip": skip,
        "fields": ",".join(attributes) if attributes else None
    }
    
    # Make the request with credentials in headers
    response = requests.get(
        base_url + "/v5/countries",
        params=params,
        headers={"Authorization": f"Bearer {credential}"}
    )
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data