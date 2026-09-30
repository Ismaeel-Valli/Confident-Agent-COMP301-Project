import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - sort_field (str): Field used for ordering the results.
    
    Returns:
        list or None: Decoded JSON response as a list, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/posts"
    
    params = {
        "limit": inputs["result_limit"],
        "sort_by": inputs["sort_field"]
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        posts = data.get("posts", [])
        
        if not posts:
            return None
        
        return posts
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")