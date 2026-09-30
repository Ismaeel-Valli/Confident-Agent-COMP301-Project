import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - included_attributes (list): Attributes to include in response
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if empty successful response
        Raises: Exception for unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5"
    
    # Build query parameters
    params = {}
    
    if inputs.get("included_attributes"):
        params["attributes"] = ",".join(inputs["included_attributes"])
    
    if inputs.get("search_text"):
        params["search"] = inputs["search_text"]
    
    # Make the request with credential in headers
    response = requests.get(
        base_url,
        params=params,
        headers={"Authorization": f"Bearer {inputs['credential']}"}
    )
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data