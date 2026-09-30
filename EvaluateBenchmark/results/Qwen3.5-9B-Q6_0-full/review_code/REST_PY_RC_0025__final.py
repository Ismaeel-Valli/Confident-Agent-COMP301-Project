import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return
            - results_to_skip (int): Number of results to skip
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5.0/countries/all"
    
    params = {
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    return data if data else None