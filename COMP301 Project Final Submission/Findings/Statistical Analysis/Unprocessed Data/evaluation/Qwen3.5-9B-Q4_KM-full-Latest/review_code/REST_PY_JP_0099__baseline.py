import requests

def solve(inputs):
    """
    Updates a todo item on JSONPlaceholder with new 'completed' status.
    
    Args:
        inputs (dict): Contains:
            - resource_id (int): ID of the todo to update.
            - new_completed (bool): New value for the completed field.
    
    Returns:
        None if successful (empty response body).
        Decoded JSON response otherwise (if applicable).
    
    Raises:
        Exception: If HTTP status code indicates failure (4xx or 5xx).
    """
    resource_id = inputs['resource_id']
    new_completed = inputs['new_completed']
    
    url = "https://jsonplaceholder.typicode.com/todos/1"
    payload = {
        "id": resource_id,
        "userId": 1,
        "title": "foo",
        "completed": new_completed
    }
    
    response = requests.patch(url, json=payload)
    
    if response.status_code == 200:
        return None
    
    raise Exception(f"Failed to update todo. Status code: {response.status_code}, Response: {response.text}")