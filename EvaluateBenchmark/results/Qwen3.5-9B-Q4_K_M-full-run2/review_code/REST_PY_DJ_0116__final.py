import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip.
            - included_fields (str): Comma-separated list of fields to return.
    
    Returns:
        dict or None: Decoded JSON response, or None for empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users"
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1,
        "fields": inputs["included_fields"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    return response.json()