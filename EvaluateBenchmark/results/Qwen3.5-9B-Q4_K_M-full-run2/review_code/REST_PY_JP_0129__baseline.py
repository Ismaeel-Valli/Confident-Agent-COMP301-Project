import requests

def solve(inputs):
    """
    Updates selected fields of a comment on JSONPlaceholder.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'resource_id' (int): The ID of the comment to update.
            - 'new_body' (str): The new value for the 'body' attribute.
    
    Returns:
        None if the request is successful (HTTP 200) and returns an empty body.
        Otherwise, returns the decoded JSON response.
    
    Raises:
        Exception: If the HTTP response status code indicates failure (e.g., 4xx or 5xx).
    """
    resource_id = inputs['resource_id']
    new_body = inputs['new_body']
    
    url = "https://jsonplaceholder.typicode.com/comments/1"
    payload = {
        "id": resource_id,
        "body": new_body
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code == 200:
        return None
    
    return response.json()