import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return
            - included_attributes (list): Attributes to include in response
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v3/countries"
    
    params = {
        "limit": inputs["result_limit"],
        "credential": inputs["credential"]
    }
    
    # Build query string with included attributes if provided
    if inputs["included_attributes"]:
        params["attributes"] = ",".join(inputs["included_attributes"])
    
    response = requests.get(f"{base_url}{endpoint}", params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data