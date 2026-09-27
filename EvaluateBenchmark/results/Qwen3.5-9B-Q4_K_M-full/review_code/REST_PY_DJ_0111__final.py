def solve(inputs):
    """Retrieve one page of todos from DummyJSON with pagination and field filtering."""
    import requests
    
    base_url = "https://dummyjson.com"
    endpoint = "/todos"
    
    result_limit = inputs.get("result_limit", 10)
    results_to_skip = inputs.get("results_to_skip", 0)
    included_fields = inputs.get("included_fields", "")
    
    # Build query parameters
    params = {
        "skip": results_to_skip,
        "limit": result_limit
    }
    
    # Handle field filtering if specified
    if included_fields:
        fields_list = [f.strip() for f in included_fields.split(",")]
        params["fields"] = ",".join(fields_list)
    
    url = base_url + endpoint
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # DummyJSON returns {"todos": [...], ...}
        return data["todos"]
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")