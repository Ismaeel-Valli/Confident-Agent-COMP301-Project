import requests


def solve(inputs):
    """
    Replaces a comment record on JSONPlaceholder with supplied data.
    
    Parameters:
        inputs (dict): Contains 'resource_id', 'new_body', 'new_email', 
                       'new_name', and 'new_post_identifier'.
    
    Returns:
        int or None: The response's id value, or None if the response is empty.
    
    Raises:
        requests.RequestException: If the HTTP request fails (non-2xx status).
    """
    resource_id = inputs['resource_id']
    new_body = inputs['new_body']
    new_email = inputs['new_email']
    new_name = inputs['new_name']
    new_post_identifier = inputs['new_post_identifier']

    url = "https://jsonplaceholder.typicode.com/comments"
    payload = {
        "id": resource_id,
        "body": new_body,
        "email": new_email,
        "name": new_name,
        "postId": new_post_identifier
    }

    response = requests.put(url, json=payload)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise requests.RequestException(f"HTTP {response.status_code}: {response.text}")

    if not response.json():
        return None
    
    return response.json().get("id")