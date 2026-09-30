import requests

def solve(inputs):
    """
    Update selected fields of a post on DummyJSON.
    
    Args:
        inputs (dict): Contains 'resource_id' and 'new_title'.
        
    Returns:
        int or None: The response's id value, or None if absent or successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    new_title = inputs['new_title']
    
    base_url = "https://dummyjson.com/posts"
    url = f"{base_url}/{resource_id}"
    
    payload = {
        "title": new_title
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to update post: HTTP {response.status_code}")
    
    data = response.json()
    
    # Check for id in the response
    if 'id' in data and data['id'] is not None:
        return data['id']
    
    # Return None for successful empty response or missing id
    return None