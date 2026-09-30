import requests

def solve(inputs):
    """
    Updates selected fields of a comment on JSONPlaceholder.
    
    Args:
        inputs (dict): A dictionary containing:
            - resource_id (int): The ID of the comment to update.
            - new_body (str): The new value for the 'body' attribute.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, 
                      None if the response is empty (204 No Content).
    
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    resource_id = inputs['resource_id']
    new_body = inputs['new_body']
    
    url = "https://jsonplaceholder.typicode.com/comments"
    payload = {
        'id': resource_id,
        'body': new_body
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code == 204:
        return None
    
    if not response.ok:
        raise requests.RequestException(f"Failed to update comment. Status code: {response.status_code}")
    
    return response.json()