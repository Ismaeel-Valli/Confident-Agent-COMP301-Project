import requests

def solve(inputs):
    """
    Submit a new post to JSONPlaceholder using the provided title.
    
    Args:
        inputs (dict): Must contain 'new_title' key with the title value.
        
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/posts"
    
    title = inputs["new_title"]
    
    payload = {
        "title": title,
        "body": "",
        "userId": 1
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create post. Status code: {response.status_code}")
    
    return None