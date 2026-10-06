import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return.
            - included_attributes (list): List of country attributes to include in the response.
            - search_text (str): Search term for filtering countries.
            - credential (str): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {}
    if inputs.get("result_limit") is not None:
        params["limit"] = inputs["result_limit"]
    if inputs.get("included_attributes") is not None:
        params["fields"] = ",".join(inputs["included_attributes"])
    if inputs.get("search_text") is not None:
        params["name"] = inputs["search_text"]
    
    # Make the request with the provided credential
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