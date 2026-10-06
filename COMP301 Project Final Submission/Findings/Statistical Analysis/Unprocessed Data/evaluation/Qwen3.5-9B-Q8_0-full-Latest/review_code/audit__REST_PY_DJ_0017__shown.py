import requests

def solve(inputs):
    """
    Search posts on DummyJSON using the provided search term.
    
    Args:
        inputs (dict): Must contain 'search_text' key with the search term.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/posts/search"
    search_text = inputs.get("search_text")
    
    params = {"q": search_text}
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (no posts found)
    if not data.get("posts"):
        return None
    
    return data