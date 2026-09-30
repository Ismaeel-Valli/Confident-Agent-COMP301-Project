def solve(inputs):
    """Retrieve one page of todos from DummyJSON with pagination and field filtering."""
    import requests
    
    base_url = "https://dummyjson.com"
    endpoint = "/todos"
    
    result_limit = inputs.get("result_limit", 10)
    results_to_skip = inputs.get("results_to_skip", 0)
    included_fields = inputs.get("included_fields", "")
    
    # Build query string for pagination and fields
    params = {
        "skip": results_to_skip,
        "limit": result_limit
    }
    
    if included_fields:
        fields_list = [f.strip() for f in included_fields.split(",")]
        params["fields"] = ",".join(fields_list)
    
    url = f"{base_url}{endpoint}"
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    return response.json()