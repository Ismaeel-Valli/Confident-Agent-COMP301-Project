import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON with pagination and sorting.
    
    Parameters:
        inputs (dict): Must contain 'results_to_skip' (int) and 'sort_field' (str).
        
    Returns:
        list or None: Decoded JSON response as a list, or None if empty.
        
    Raises:
        Exception: If HTTP request fails.
    """
    base_url = "https://dummyjson.com/posts"
    
    # Validate inputs
    results_to_skip = inputs.get("results_to_skip")
    sort_field = inputs.get("sort_field")
    
    if results_to_skip is None or sort_field is None:
        raise ValueError("Missing required inputs: 'results_to_skip' and 'sort_field'")
    
    params = {
        "skip": results_to_skip,
        "limit": 1,  # Retrieve one page (one result)
        "sort_by": sort_field
    }
    
    response = requests.get(base_url, params=params)
    
    if not response.ok:
        raise Exception(f"HTTP request failed with status {response.status_code}")
    
    data = response.json()
    
    # Return the list of posts (or None if empty)
    return data.get("posts")