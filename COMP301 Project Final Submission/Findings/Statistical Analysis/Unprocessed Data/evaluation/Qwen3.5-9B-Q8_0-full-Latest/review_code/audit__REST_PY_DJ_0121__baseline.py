import requests

def solve(inputs):
    """
    Updates selected fields of a todo in DummyJSON API.
    
    Args:
        inputs (dict): Contains 'resource_id', 'new_todo', and 'new_user_identifier'.
        
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    resource_id = inputs['resource_id']
    new_todo = inputs['new_todo']
    new_user_identifier = inputs['new_user_identifier']
    
    # Base URL for DummyJSON API
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/todos/{resource_id}"
    
    # Prepare the payload with only the fields to update
    payload = {
        "todo": new_todo,
        "userId": new_user_identifier
    }
    
    # Send PATCH request
    response = requests.patch(url, json=payload)
    
    # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
    response.raise_for_status()
    
    # Return None if the response is empty (204 No Content)
    if response.status_code == 204:
        return None
    
    # Decode and return the JSON response
    return response.json()