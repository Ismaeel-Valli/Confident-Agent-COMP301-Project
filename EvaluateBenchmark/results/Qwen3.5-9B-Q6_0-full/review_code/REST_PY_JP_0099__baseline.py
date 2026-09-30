import requests

def solve(inputs):
    """
    Updates a todo item in JSONPlaceholder based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - resource_id (int): The ID of the todo to update.
            - new_completed (bool): The new value for the 'completed' field.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, otherwise None.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    resource_id = inputs['resource_id']
    new_completed = inputs['new_completed']
    
    url = "https://jsonplaceholder.typicode.com/todos/1"
    payload = {
        "id": resource_id,
        "title": "foo",
        "userId": 1,
        "completed": new_completed
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    return response.json() if response.content else None