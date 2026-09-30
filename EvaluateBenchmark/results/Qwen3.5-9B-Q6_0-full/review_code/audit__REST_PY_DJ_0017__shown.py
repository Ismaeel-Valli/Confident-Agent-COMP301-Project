import requests

def solve(inputs):
    """Search posts on DummyJSON using the provided search term."""
    base_url = "https://dummyjson.com/posts/search"
    params = {"q": inputs["search_text"]}
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raises an exception for unsuccessful HTTP responses
    
    data = response.json()
    
    # Return None if the response is successful but empty (no posts found)
    if not data.get("posts"):
        return None
    
    return data