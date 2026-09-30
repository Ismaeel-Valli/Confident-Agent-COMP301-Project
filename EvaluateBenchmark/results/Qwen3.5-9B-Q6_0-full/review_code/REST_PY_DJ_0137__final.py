import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to return
            - sort_field (str): Field used for ordering
    
    Returns:
        dict or None: Decoded JSON response, or None if empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/posts"
    
    # Parse included_fields
    fields_list = [f.strip() for f in inputs["included_fields"].split(",")]
    
    params = {
        "include_fields": ",".join(fields_list),
        "sort_by": inputs["sort_field"],
        "limit": 1,  # Retrieve one page (one post)
        "skip": 0
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    # Return None for empty response (no posts found)
    if not data.get("posts"):
        return None
    
    return data