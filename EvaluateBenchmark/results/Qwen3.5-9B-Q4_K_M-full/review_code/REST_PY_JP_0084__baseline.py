import requests

def solve(inputs):
    """
    Replaces a todo record on JSONPlaceholder with the supplied data.
    
    Inputs:
        inputs['resource_id']: Identifier of the todo (id)
        inputs['new_completed']: value for the completed attribute
        inputs['new_title']: value for the title attribute
        inputs['new_user_identifier']: value for the user Id attribute
    
    Returns:
        The response's 'title' value if present, or None if absent.
        Returns None for a successful empty response (204 No Content).
    
    Raises:
        Exception for unsuccessful HTTP responses (non-2xx status codes).
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
    
    if response.status_code == 204:
        return None
    
    if response.status_code != 200:
        raise Exception(f"Failed to update todo. Status code: {response.status_code}, Response: {response.text}")

    data = response.json()
    title = data.get('title')
    
    return title