def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON with filtering by limit and fields.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - included_fields (str): Comma-separated list of fields to include in the response.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    base_url = "https://dummyjson.com"
    endpoint = "/todos"
    url = f"{base_url}{endpoint}"
    
    params = {
        "limit": inputs["result_limit"],
        "_fields": inputs["included_fields"]
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error {response.status_code}: {response.text}")
    
    return response.json()