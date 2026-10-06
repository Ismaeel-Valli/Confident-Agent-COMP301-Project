import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - sort_field (str): Field used for ordering the results.
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/posts"
    params = {
        "limit": inputs["result_limit"],
        "sort": inputs["sort_field"]
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # DummyJSON returns a dict with 'posts' key and 'total' count.
        # If the posts list is empty, return None as per requirement.
        if not data.get("posts"):
            return None
        
        return data
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")