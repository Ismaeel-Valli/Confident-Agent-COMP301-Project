import requests

def solve(inputs):
    """
    Updates a todo item's title in JSONPlaceholder and returns the new title.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'resource_id' (int): The ID of the todo to update.
            - 'new_title' (str): The new title for the todo.
    
    Returns:
        str or None: The updated title if present in the response, otherwise None.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    resource_id = inputs['resource_id']
    new_title = inputs['new_title']
    
    url = "https://jsonplaceholder.typicode.com/todos/1"
    payload = {
        "id": resource_id,
        "title": new_title,
        "completed": False
    }
    
    response = requests.patch(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update todo: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return data.get('title')