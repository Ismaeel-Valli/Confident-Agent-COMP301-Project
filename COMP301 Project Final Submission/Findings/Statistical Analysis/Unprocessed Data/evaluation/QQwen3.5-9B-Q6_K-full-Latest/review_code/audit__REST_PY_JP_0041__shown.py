import requests


def solve(inputs):
    """
    Update a post in JSONPlaceholder by changing its title.
    
    Args:
        inputs (dict): Must contain 'resource_id' and 'new_title'.
        
    Returns:
        int or None: The response's id if present, otherwise None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs.get('resource_id')
    new_title = inputs.get('new_title')
    
    if resource_id is None or new_title is None:
        raise ValueError("Missing required inputs: 'resource_id' and 'new_title'")
    
    url = f"https://jsonplaceholder.typicode.com/posts/{resource_id}"
    payload = {
        "title": new_title
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    if data is None or 'id' not in data:
        return None
    
    return data['id']