import requests

def solve(inputs):
    """
    Submit a new todo to DummyJSON and return its id.
    
    inputs:
        - new_completed: value for the completed attribute (bool)
        - new_todo: value for the todo attribute (str)
        - new_user_identifier: value for the userId attribute (int)
    
    Returns:
        - The response's id value (int), or None if absent.
        - None for a successful empty response.
        - Raises an exception for unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/todos/add"
    
    payload = {
        "todo": inputs["new_todo"],
        "completed": inputs["new_completed"],
        "userId": inputs["new_user_identifier"]
    }
    
    response = requests.post(base_url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create todo. Status code: {response.status_code}")
    
    data = response.json()
    
    if data is None or len(data) == 0:
        return None
    
    return data.get("id")