import requests

def solve(inputs):
    """
    Update a todo item in JSONPlaceholder.
    
    Args:
        inputs (dict): Must contain 'resource_id' and 'new_completed'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    new_completed = inputs['new_completed']
    
    url = f"https://jsonplaceholder.typicode.com/todos/{resource_id}"
    payload = {
        "completed": new_completed
    }
    
    response = requests.put(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    return response.json()