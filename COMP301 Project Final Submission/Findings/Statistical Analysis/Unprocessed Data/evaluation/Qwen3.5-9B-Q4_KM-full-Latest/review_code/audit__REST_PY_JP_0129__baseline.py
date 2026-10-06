import requests

def solve(inputs):
    """
    Updates a comment on JSONPlaceholder with a new body value.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'resource_id' (int): The ID of the comment to update.
            - 'new_body' (str): The new content for the comment's body field.
            
    Returns:
        None if the request is successful (HTTP 200 OK with empty JSON response).
        
    Raises:
        requests.RequestException: If the HTTP request fails (non-2xx status code).
    """
    resource_id = inputs['resource_id']
    new_body = inputs['new_body']
    
    url = f"https://jsonplaceholder.typicode.com/comments/{resource_id}"
    payload = {"body": new_body}
    
    response = requests.put(url, json=payload)
    
    if response.status_code == 200:
        # JSONPlaceholder returns an empty object {} on successful update
        return None
    
    raise requests.RequestException(f"Failed to update comment. Status code: {response.status_code}")