import requests

def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - included_fields (str): Comma-separated list of fields to include in the response.
    
    Returns:
        dict or None: Decoded JSON response if successful, or None for an empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com"
    endpoint = "/todos"
    
    params = {
        "limit": inputs["result_limit"],
        "fields": inputs["included_fields"]
    }
    
    response = requests.get(f"{base_url}{endpoint}", params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: status code {response.status_code}")
    
    return response.json()