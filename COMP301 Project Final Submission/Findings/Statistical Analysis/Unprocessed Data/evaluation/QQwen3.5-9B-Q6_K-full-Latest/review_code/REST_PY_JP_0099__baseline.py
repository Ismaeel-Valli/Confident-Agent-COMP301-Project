import requests

def solve(inputs):
    """
    Updates a todo item in JSONPlaceholder with new completion status.
    
    Args:
        inputs (dict): Contains 'resource_id' (int) and 'new_completed' (bool).
        
    Returns:
        dict or None: Decoded JSON response if successful, None for empty body.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
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
    
    if response.status_code != 200:
        raise requests.RequestException(f"Failed to update todo. Status code: {response.status_code}")
    
    return response.json() if response.text else None