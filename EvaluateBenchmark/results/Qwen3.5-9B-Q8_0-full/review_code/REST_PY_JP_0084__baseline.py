import requests

def solve(inputs):
    """
    Replaces a todo record in JSONPlaceholder with supplied data.
    
    Args:
        inputs (dict): Contains 'resource_id', 'new_completed', 'new_title', 'new_user_identifier'.
        
    Returns:
        str or None: The title from the response, or None if successful but empty.
        
    Raises:
        requests.RequestException: If the HTTP request is unsuccessful.
    """
    resource_id = inputs['resource_id']
    new_completed = inputs['new_completed']
    new_title = inputs['new_title']
    new_user_identifier = inputs['new_user_identifier']
    
    url = "https://jsonplaceholder.typicode.com/todos/1"
    
    payload = {
        'id': resource_id,
        'title': new_title,
        'completed': new_completed,
        'userId': new_user_identifier
    }
    
    response = requests.put(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    try:
        data = response.json()
        return data.get('title')
    except ValueError:
        return None