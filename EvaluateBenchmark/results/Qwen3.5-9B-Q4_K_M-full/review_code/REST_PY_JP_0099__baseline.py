import requests

def solve(inputs):
    """
    Updates a todo item on JSONPlaceholder with new 'completed' status.
    
    Args:
        inputs (dict): Contains:
            - resource_id (int): The ID of the todo to update.
            - new_completed (bool): The new value for the completed field.
    
    Returns:
        None if the request is successful and returns an empty body.
        The decoded JSON response otherwise.
    
    Raises:
        Exception: If the HTTP response indicates failure (status code not in 2xx).
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
    
    if response.status_code == 204:
        return None
    
    if not (200 <= response.status_code < 300):
        raise Exception(f"Failed to update todo. Status code: {response.status_code}, Response: {response.text}")
    
    return response.json()