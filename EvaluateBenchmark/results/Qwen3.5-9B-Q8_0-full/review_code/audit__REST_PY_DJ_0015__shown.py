import requests

def solve(inputs):
    """
    Update selected fields of a post on DummyJSON.
    
    Args:
        inputs (dict): Contains 'resource_id' (post ID) and 'new_title' (new title).
        
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    new_title = inputs['new_title']
    
    url = f"https://dummyjson.com/posts/{resource_id}"
    
    payload = {
        "title": new_title
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to update post: HTTP {response.status_code}")
    
    return response.json() if response.content else None