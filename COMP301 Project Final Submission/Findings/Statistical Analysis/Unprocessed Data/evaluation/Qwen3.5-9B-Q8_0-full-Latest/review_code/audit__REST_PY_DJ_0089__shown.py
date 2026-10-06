import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON with pagination.
    
    Args:
        inputs (dict): Must contain 'result_limit' and 'results_to_skip'.
        
    Returns:
        dict or None: Decoded JSON response, or None if empty.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/posts"
    
    result_limit = inputs.get("result_limit")
    results_to_skip = inputs.get("results_to_skip")
    
    # Validate inputs
    if result_limit is None or results_to_skip is None:
        raise ValueError("Missing required inputs: 'result_limit' and 'results_to_skip'")
    
    params = {
        "limit": result_limit,
        "skip": results_to_skip
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (posts array is empty)
    if not data.get("posts"):
        return None
    
    return data