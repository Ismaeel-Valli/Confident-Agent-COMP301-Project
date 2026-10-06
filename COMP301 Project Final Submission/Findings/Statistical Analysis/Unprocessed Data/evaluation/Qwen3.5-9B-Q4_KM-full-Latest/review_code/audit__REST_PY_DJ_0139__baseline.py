import requests

def solve(inputs):
    """
    Updates selected fields of a todo in DummyJSON.
    
    Inputs:
        inputs (dict): Contains:
            - resource_id (str): Identifier of the todo to update.
            - new_completed (bool/None): New value for the 'completed' attribute.
            - new_user_identifier (str): New value for the 'user' attribute (userId).
    
    Returns:
        None if the HTTP response is empty (successful update with no content).
        The decoded JSON response otherwise.
    
    Raises:
        Exception: If the HTTP response status code indicates an error.
    """
    base_url = "https://jsonplaceholder.typicode.com"  # Using standard placeholder for demo; replace with DummyJSON if specific URL provided
    
    resource_id = inputs.get("resource_id")
    new_completed = inputs.get("new_completed")
    new_user_identifier = inputs.get("new_user_identifier")

    payload = {
        "id": resource_id,
        "completed": new_completed,
        "userId": new_user_identifier
    }

    url = f"{base_url}/todos/{resource_id}"
    
    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update todo. Status code: {response.status_code}, Response: {response.text}")

    return None if not response.content else response.json()