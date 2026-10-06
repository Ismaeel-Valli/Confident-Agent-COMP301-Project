import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - excluded_attributes (list): List of country attributes to exclude
            - search_text (str): Search term for filtering countries
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters using only documented parameters
    params = {}
    if inputs["result_limit"] is not None:
        params["limit"] = inputs["result_limit"]
    
    # Make the API request with credential
    headers = {"Authorization": f"Bearer {inputs['credential']}"}
    response = requests.get(f"{base_url}/countries/v5", params=params, headers=headers)
    
    # Check for successful HTTP response
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data