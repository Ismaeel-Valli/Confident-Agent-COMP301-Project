def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON, skipping specified results and returning only requested fields.
    
    Args:
        inputs (dict): Dictionary containing:
            - 'results_to_skip' (int): Number of results to skip.
            - 'included_fields' (str): Comma-separated list of fields to return.
    
    Returns:
        dict or None: Decoded JSON response, or None for a successful empty response.
    
    Raises:
        Exception: For an unsuccessful HTTP response.
    """
    import requests
    
    base_url = "https://dummyjson.com/posts"
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1,
        "_fields": inputs["included_fields"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    return response.json()