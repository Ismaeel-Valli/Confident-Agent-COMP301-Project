import requests

def solve(inputs):
    """
    Update a user's name in JSONPlaceholder.
    
    Args:
        inputs (dict): Must contain 'resource_id' (user ID) and 'new_name' (new name).
        
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty body.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    resource_id = inputs['resource_id']
    new_name = inputs['new_name']
    
    url = f"https://jsonplaceholder.typicode.com/users/{resource_id}"
    payload = {
        "name": new_name
    }
    
    response = requests.patch(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update user: {response.status_code} - {response.text}")
    
    return None