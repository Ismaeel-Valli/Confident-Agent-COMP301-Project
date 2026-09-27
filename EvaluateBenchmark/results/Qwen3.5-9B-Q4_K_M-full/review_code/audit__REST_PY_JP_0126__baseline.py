import requests

def solve(inputs):
    """
    Submits a new post to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'new_title': The title for the new post.
            - 'new_user_identifier': The user ID for the new post.
    
    Returns:
        None if the response is empty (successful submission).
        The decoded JSON response otherwise.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {
        "title": inputs["new_title"],
        "body": "",  # Body is optional, but we'll leave it empty as per typical minimal post creation
        "userId": inputs["new_user_identifier"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create post. Status code: {response.status_code}, Response: {response.text}")
    
    # JSONPlaceholder returns an empty body for POST requests on /posts
    if not response.text.strip():
        return None
    
    return response.json()