import requests

def solve(inputs):
    """
    Update selected fields of a todo in DummyJSON.
    
    Args:
        inputs (dict): Contains:
            - resource_id (int): Identifier of the todo to update
            - new_todo (str): New value for the 'todo' attribute
            - new_user_identifier (int): New value for the 'userId' attribute
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com"
    todo_id = inputs["resource_id"]
    new_todo_value = inputs["new_todo"]
    new_user_id = inputs["new_user_identifier"]
    
    url = f"{base_url}/todos/{todo_id}"
    
    payload = {
        "todo": new_todo_value,
        "userId": new_user_id
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update todo. Status code: {response.status_code}")
    
    return response.json() if response.content else None