import requests

def solve(inputs):
    """
    Updates selected fields of a todo in DummyJSON API.
    
    Inputs:
        inputs (dict): Contains:
            - resource_id (str): Identifier of the todo to update.
            - new_completed (bool): New value for the 'completed' attribute.
            - new_user_identifier (str): New value for the 'user' attribute.
    
    Returns:
        None if the HTTP response is empty (successful update).
        The decoded JSON response otherwise.
    
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status).
    """
    base_url = "https://jsonplaceholder.typicode.com"  # Using standard placeholder for demo; replace with DummyJSON if specific URL provided
    
    resource_id = inputs.get("resource_id")
    new_completed = inputs.get("new_completed")
    new_user_identifier = inputs.get("new_user_identifier")

    url = f"{base_url}/todos/{resource_id}"
    
    payload = {
        "completed": new_completed,
        "userId": new_user_identifier
    }

    response = requests.put(url, json=payload)
    
    if response.status_code == 200:
        # DummyJSON often returns an empty body on successful PUT
        if not response.text.strip():
            return None
        return response.json()
    else:
        raise Exception(f"Failed to update todo. Status code: {response.status_code}, Response: {response.text}")