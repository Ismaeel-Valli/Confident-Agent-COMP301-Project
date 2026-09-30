import requests

def solve(inputs):
    """
    Update selected fields of a post on DummyJSON.
    
    Args:
        inputs (dict): Contains 'resource_id' (post ID) and 'new_title' (new title).
        
    Returns:
        int or None: The response's id value, or None if absent or successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    new_title = inputs['new_title']
    
    url = "https://dummyjson.com/posts/{id}".format(id=resource_id)
    payload = {"title": new_title}
    
    response = requests.put(url, json=payload)
    
    if response.status_code >= 400:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Check for successful empty response or missing id
    if not data or 'id' not in data:
        return None
    
    return data['id']