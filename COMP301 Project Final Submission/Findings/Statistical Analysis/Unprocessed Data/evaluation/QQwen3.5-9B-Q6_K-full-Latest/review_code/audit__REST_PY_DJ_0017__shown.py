import requests

def solve(inputs):
    """
    Search posts on DummyJSON using the provided search term.
    
    Args:
        inputs (dict): Must contain 'search_text' key with the search term.
        
    Returns:
        list or None: Decoded JSON response as a list of posts, or None if empty.
        
    Raises:
        requests.RequestException: If HTTP request fails.
    """
    base_url = "https://dummyjson.com/posts/search"
    search_text = inputs.get("search_text")
    
    if not search_text:
        raise ValueError("Missing or empty 'search_text' in inputs.")
    
    params = {"q": search_text}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    data = response.json()
    posts = data.get("posts", [])
    
    if not posts:
        return None
    
    return posts