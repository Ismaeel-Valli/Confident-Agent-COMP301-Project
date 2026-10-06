import requests

def solve(inputs):
    """
    Submit a new todo to DummyJSON API.
    
    Args:
        inputs (dict): Dictionary containing:
            - new_completed: value for the completed attribute
            - new_todo: value for the todo attribute
            - new_user_identifier: value for the user Id attribute
    
    Returns:
        dict or None: Decoded JSON response, or None if successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com"
    url = f"{base_url}/todos/add"
    
    payload = {
        "userId": inputs["new_user_identifier"],
        "title": inputs["new_todo"],
        "completed": inputs["new_completed"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create todo. Status code: {response.status_code}")
    
    return response.json()