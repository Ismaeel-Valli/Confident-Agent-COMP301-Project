import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON.
    
    Args:
        inputs (dict): Must contain 'result_limit' (int) specifying max results.
        
    Returns:
        list or None: Decoded JSON response as a list, or None for empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/posts"
    result_limit = inputs.get("result_limit")
    
    if result_limit is None:
        raise ValueError("Missing required parameter: result_limit")
    
    params = {"limit": result_limit}
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    # DummyJSON returns a dict with 'posts' key containing the list
    posts = data.get("posts", [])
    
    return posts if posts else None