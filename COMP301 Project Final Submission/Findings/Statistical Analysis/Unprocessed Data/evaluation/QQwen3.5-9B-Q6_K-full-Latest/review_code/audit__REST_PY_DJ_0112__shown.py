import requests

def solve(inputs):
    """
    Update selected fields of a todo in DummyJSON.
    
    Args:
        inputs (dict): Contains:
            - resource_id (int): ID of the todo to update
            - new_completed (bool): New value for completed attribute
            - new_todo (str): New value for todo attribute
    
    Returns:
        int or None: The response's id value, or None if absent or successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/todos"
    resource_id = inputs["resource_id"]
    new_completed = inputs["new_completed"]
    new_todo = inputs["new_todo"]
    
    payload = {
        "todo": new_todo,
        "completed": new_completed
    }
    
    response = requests.put(f"{base_url}/{resource_id}", json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    # Check for id in the response
    if "id" in data and data["id"] is not None:
        return data["id"]
    elif data == {}:
        return None
    else:
        return None