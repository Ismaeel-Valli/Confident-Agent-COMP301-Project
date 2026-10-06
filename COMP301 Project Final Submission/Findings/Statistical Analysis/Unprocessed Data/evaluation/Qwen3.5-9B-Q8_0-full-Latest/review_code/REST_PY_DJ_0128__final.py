import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON with pagination and sorting.
    
    Args:
        inputs (dict): Must contain:
            - results_to_skip (int): Number of results to skip (offset)
            - sort_field (str): Field used for ordering
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/posts"
    
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1,  # Retrieve one page (one result)
        "sort_by": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    # Return None for a successful empty response (no posts found)
    if not data.get("posts"):
        return None
    
    return data