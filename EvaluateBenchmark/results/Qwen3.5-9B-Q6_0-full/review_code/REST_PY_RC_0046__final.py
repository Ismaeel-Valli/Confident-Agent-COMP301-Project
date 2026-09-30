import requests

def solve(inputs):
    """
    Search country names using REST Countries v5 API.
    
    Parameters:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip.
            - excluded_attributes (list): List of attributes to exclude from each country object.
            - search_text (str): Search term for country names.
            - credential (str): Caller-supplied API credential (assumed valid).
    
    Returns:
        dict or None: Decoded JSON response. Returns None if the response is successfully empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (non-2xx status code).
    """
    base_url = "https://api.restcountries.com/v5"
    endpoint = "/search"
    
    # Build query parameters
    params = {
        "name": inputs["search_text"],
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    # Prepare headers with the provided credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    # Make the GET request
    response = requests.get(f"{base_url}{endpoint}", params=params, headers=headers)
    
    # Check for unsuccessful HTTP response
    if not response.ok:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for a successful empty response
    if len(data) == 0:
        return None
    
    return data