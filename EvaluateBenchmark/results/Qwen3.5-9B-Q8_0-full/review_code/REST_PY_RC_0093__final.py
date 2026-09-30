import requests

def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The region to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to include in response
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty response
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {
        "region": inputs["value"],
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    # Determine which attributes to include
    if inputs["included_attributes"]:
        params["fields"] = ",".join(inputs["included_attributes"])
    
    # Make the API request with credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(
        f"{base_url}/v5/countries",
        params=params,
        headers=headers
    )
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response, otherwise return the list
    if not data:
        return None
    
    return data