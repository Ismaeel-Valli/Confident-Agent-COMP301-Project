import requests

def solve(inputs):
    """
    Updates a todo item on JSONPlaceholder with a new title and returns the updated title.
    
    Parameters:
        inputs (dict): A dictionary containing:
            - resource_id (int): The ID of the todo to update.
            - new_title (str): The new title for the todo.
    
    Returns:
        str or None: The updated title if present, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response indicates an error (status code >= 400).
    """
    resource_id = inputs["resource_id"]
    new_title = inputs["new_title"]
    
    url = "https://jsonplaceholder.typicode.com/todos/1"
    payload = {
        "id": resource_id,
        "title": new_title
    }
    
    response = requests.patch(url, json=payload)
    
    if response.status_code >= 400:
        raise Exception(f"HTTP Error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data.get("title")