import requests

def solve(inputs):
    """
    Submits a new post to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'new_title': The title for the new post.
            - 'new_user_identifier': The user ID for the new post.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, 
                      None if the response is empty (204 No Content).
    
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    
    payload = {
        "title": inputs['new_title'],
        "body": "",  # JSONPlaceholder requires a body field, even if empty
        "userId": inputs['new_user_identifier']
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 201:
        return response.json()
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Failed to create post. Status code: {response.status_code}, Response: {response.text}")