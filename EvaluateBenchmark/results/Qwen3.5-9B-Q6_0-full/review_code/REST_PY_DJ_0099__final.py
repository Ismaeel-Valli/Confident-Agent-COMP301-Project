def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON with pagination and field filtering.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - included_fields (str): Comma-separated list of fields to include
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    base_url = "https://dummyjson.com/posts"
    
    # Parse included_fields
    if inputs.get("included_fields"):
        fields = [f.strip() for f in inputs["included_fields"].split(",")]
        params = {"limit": inputs["result_limit"], "fields": ",".join(fields)}
    else:
        params = {"limit": inputs["result_limit"]}
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # DummyJSON returns empty dict for no posts, not None
    if not data:
        return None
    
    return data