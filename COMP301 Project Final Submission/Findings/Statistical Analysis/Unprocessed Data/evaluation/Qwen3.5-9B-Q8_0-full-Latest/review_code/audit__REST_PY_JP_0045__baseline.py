import requests

def solve(inputs):
    """
    Replaces a comment record on JSONPlaceholder with supplied data.
    
    Args:
        inputs (dict): Contains 'resource_id', 'new_body', 'new_email', 
                       'new_name', and 'new_post_identifier'.
    
    Returns:
        int or None: The ID of the updated comment, or None if the response is empty.
                     Raises an exception for unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    new_body = inputs['new_body']
    new_email = inputs['new_email']
    new_name = inputs['new_name']
    new_post_identifier = inputs['new_post_identifier']

    url = "https://jsonplaceholder.typicode.com/comments"
    
    payload = {
        'id': resource_id,
        'body': new_body,
        'email': new_email,
        'name': new_name,
        'postId': new_post_identifier
    }

    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data.get('id')