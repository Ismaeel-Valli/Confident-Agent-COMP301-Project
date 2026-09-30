import requests

def solve(inputs):
    """
    Updates selected fields of a post on JSONPlaceholder.
    
    Args:
        inputs (dict): A dictionary containing:
            - resource_id (int): The ID of the post to update.
            - new_user_identifier (int): The new value for the 'userId' attribute.
    
    Returns:
        None if the response is empty (successful update).
        The decoded JSON response otherwise.
    
    Raises:
        Exception: If the HTTP response status code indicates an error.
    """
    resource_id = inputs['resource_id']
    new_user_identifier = inputs['new_user_identifier']
    
    url = f"https://jsonplaceholder.typicode.com/posts/{resource_id}"
    payload = {
        "userId": new_user_identifier
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code} - {response.text}")
    
    return None