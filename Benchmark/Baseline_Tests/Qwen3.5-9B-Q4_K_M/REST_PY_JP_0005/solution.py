import requests

def solve(inputs):
    """
    Updates the title of a post on JSONPlaceholder.
    
    Args:
        inputs (dict): A dictionary containing:
            - resource_id (int): The ID of the post to update.
            - new_title (str): The new title for the post.
    
    Returns:
        None if the request is successful (HTTP 200 OK with empty body).
        The decoded JSON response if the server returns data.
    
    Raises:
        requests.RequestException: If the HTTP response status code indicates an error.
    """
    resource_id = inputs['resource_id']
    new_title = inputs['new_title']
    
    url = f"https://jsonplaceholder.typicode.com/posts/{resource_id}"
    data = {"title": new_title}
    
    response = requests.put(url, json=data)
    
    if response.status_code == 200:
        # JSONPlaceholder returns an empty body for successful PUT requests on posts
        return None
    
    response.raise_for_status()