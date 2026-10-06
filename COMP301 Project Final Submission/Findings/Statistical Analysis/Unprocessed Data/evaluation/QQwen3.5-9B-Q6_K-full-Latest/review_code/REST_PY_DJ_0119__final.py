import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON with pagination and field filtering.
    
    Args:
        inputs (dict): Must contain:
            - results_to_skip (int): Number of results to skip (for pagination)
            - included_fields (str): Comma-separated list of fields to include
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/posts"
    results_to_skip = inputs.get("results_to_skip", 0)
    included_fields = inputs.get("included_fields", "")
    
    # Build query parameters
    params = {
        "skip": results_to_skip,
        "limit": 1,  # Retrieve one page (one result)
    }
    
    if included_fields:
        fields_list = [f.strip() for f in included_fields.split(",")]
        params["fields"] = ",".join(fields_list)
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # DummyJSON returns a dict with 'posts' key; return the posts list
    return data.get("posts")