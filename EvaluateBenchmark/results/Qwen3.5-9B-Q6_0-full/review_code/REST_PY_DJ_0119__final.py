def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON with pagination and field filtering.
    
    Args:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip (for pagination)
            - included_fields (str): Comma-separated list of fields to include
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    base_url = "https://dummyjson.com/posts"
    
    # Parse included_fields
    if inputs.get("included_fields"):
        fields_list = [f.strip() for f in inputs["included_fields"].split(",")]
    else:
        fields_list = []
    
    # Build query parameters
    params = {
        "skip": inputs.get("results_to_skip", 0),
        "limit": 1,  # Retrieve one page (one result)
    }
    
    if fields_list:
        params["fields"] = ",".join(fields_list)
    
    try:
        response = requests.get(base_url, params=params)
        
        # Raise exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode JSON response
        data = response.json()
        
        # Return None for successful empty response
        if not data.get("posts") or len(data["posts"]) == 0:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")