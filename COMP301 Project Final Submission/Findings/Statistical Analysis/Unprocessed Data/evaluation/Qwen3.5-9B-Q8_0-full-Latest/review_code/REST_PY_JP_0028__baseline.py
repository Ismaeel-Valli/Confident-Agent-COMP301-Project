import requests

def solve(inputs):
    """
    Replaces a todo record in JSONPlaceholder with supplied data.
    
    Args:
        inputs (dict): Contains 'resource_id', 'new_completed', 'new_title', 'new_user_identifier'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful and response is empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
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
    
    if response.status_code != 200:
        raise Exception(f"Failed to update todo. Status code: {response.status_code}, Response: {response.text}")
    
    return response.json() if response.content else None