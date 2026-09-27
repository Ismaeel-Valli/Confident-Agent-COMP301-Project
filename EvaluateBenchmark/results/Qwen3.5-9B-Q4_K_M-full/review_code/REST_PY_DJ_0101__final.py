def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip.
            - included_fields (str): Fields to return, separated by commas.
    
    Returns:
        dict or None: Decoded JSON response, or None for a successful empty response.
    
    Raises:
        Exception: For an unsuccessful HTTP response.
    """
    import requests
    
    base_url = "https://dummyjson.com"
    endpoint = "/todos"
    
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1,
        "_fields": inputs["included_fields"]
    }
    
    response = requests.get(f"{base_url}{endpoint}", params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error {response.status_code}: {response.text}")
    
    return response.json()