import requests

def solve(inputs):
    """
    Update selected fields of a todo in DummyJSON.
    
    Args:
        inputs (dict): Contains:
            - resource_id (int): ID of the todo to update
            - new_todo (str): New value for the 'todo' attribute
            - new_user_identifier (int): New value for the 'userId' attribute
    
    Returns:
        int or None: The response's id value, or None if absent or successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/todos"
    resource_id = inputs["resource_id"]
    new_todo = inputs["new_todo"]
    new_user_identifier = inputs["new_user_identifier"]
    
    payload = {
        "todo": new_todo,
        "userId": new_user_identifier
    }
    
    response = requests.put(f"{base_url}/{resource_id}", json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return the id from the response, or None if absent
    return data.get("id")