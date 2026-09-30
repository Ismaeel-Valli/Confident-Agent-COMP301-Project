def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON, skipping specified results and filtering fields.
    
    Args:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip
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
        fields_list = [f.strip() for f in inputs["included_fields"].split(",")]
    else:
        fields_list = None
    
    params = {
        "skip": inputs.get("results_to_skip", 0),
        "limit": 1,  # Retrieve one page
    }
    
    if fields_list:
        params["fields"] = ",".join(fields_list)
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # DummyJSON posts endpoint returns a list directly (not wrapped in a dict with 'posts' key)
    return data if data else None