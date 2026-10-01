import requests

def solve(inputs):
    """
    Submit a new post to JSONPlaceholder using the provided title.
    
    Args:
        inputs (dict): Must contain 'new_title' key with the post title string.
        
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/posts"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": inputs["new_title"]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create post. Status code: {response.status_code}, Response: {response.text}")
    
    return None