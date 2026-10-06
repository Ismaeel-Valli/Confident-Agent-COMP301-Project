import requests

def solve(inputs):
    """
    Updates selected fields of a todo in DummyJSON API.
    
    Args:
        inputs (dict): Contains 'resource_id', 'new_completed', and 'new_user_identifier'.
        
    Returns:
        dict or None: Decoded JSON response, or None if response is empty.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    resource_id = inputs['resource_id']
    new_completed = inputs['new_completed']
    new_user_identifier = inputs['new_user_identifier']
    
    url = f"https://jsonplaceholder.typicode.com/todos/{resource_id}"
    
    payload = {
        "completed": new_completed,
        "userId": new_user_identifier
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update todo. Status code: {response.status_code}, Response: {response.text}")
    
    if len(response.content) == 0:
        return None
    
    return response.json()