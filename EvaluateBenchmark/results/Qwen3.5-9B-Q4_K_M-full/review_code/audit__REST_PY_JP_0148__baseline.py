import requests

def solve(inputs):
    """
    Submits a new post to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'new_title': The title for the new post.
            - 'new_user_identifier': The user ID for the new post.
    
    Returns:
        str or None: The title of the created post if present in the response, 
                     otherwise None for a successful empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx range).
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {
        "title": inputs["new_title"],
        "body": "",  # JSONPlaceholder requires a body field, but we can leave it empty.
        "userId": inputs["new_user_identifier"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    # Check if the response contains a 'title' attribute
    data = response.json()
    if isinstance(data, dict) and "title" in data:
        return data["title"]
    else:
        return None