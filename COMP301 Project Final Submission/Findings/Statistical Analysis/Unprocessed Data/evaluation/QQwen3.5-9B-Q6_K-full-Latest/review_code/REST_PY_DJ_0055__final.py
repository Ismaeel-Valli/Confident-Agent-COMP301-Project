import requests

def solve(inputs):
    """
    Update selected fields of a post on DummyJSON.
    
    Args:
        inputs (dict): Contains 'resource_id' (post ID) and 'new_title' (new title).
        
    Returns:
        str or None: The updated post's title, or None if absent or response is empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs.get('resource_id')
    new_title = inputs.get('new_title')
    
    if resource_id is None or new_title is None:
        raise ValueError("Missing required input fields: resource_id and new_title")
    
    url = "https://dummyjson.com/posts/{id}".format(id=resource_id)
    
    payload = {
        "title": new_title
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # DummyJSON returns the updated post in 'post' field for PATCH requests
    if 'post' in data and data['post'] is not None:
        return data['post'].get('title')
    elif data.get('message'):
        # Empty or informational response
        return None
    else:
        return None