import requests


def solve(inputs):
    """
    Updates a todo item in JSONPlaceholder with new completion status.
    
    Args:
        inputs (dict): Contains 'resource_id' (int) and 'new_completed' (bool).
        
    Returns:
        int or None: The ID of the updated todo, or None if response is empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    resource_id = inputs['resource_id']
    new_completed = inputs['new_completed']
    
    url = "https://jsonplaceholder.typicode.com/todos/1"
    payload = {
        "id": resource_id,
        "completed": new_completed
    }
    
    response = requests.patch(url, json=payload)
    
    if response.status_code != 200:
        raise requests.RequestException(f"Failed to update todo: {response.status_code}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data.get('id')