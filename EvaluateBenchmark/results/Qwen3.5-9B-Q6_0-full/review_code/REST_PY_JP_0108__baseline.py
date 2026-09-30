import requests

def solve(inputs):
    """
    Submits a new photo to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing 'new_title' and 'new_url'.
        
    Returns:
        int or None: The ID of the created post, or None if the response is empty/successful without an ID.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    
    payload = {
        "title": inputs.get("new_title"),
        "body": "",  # JSONPlaceholder requires a body for posts, though not specified in prompt, we provide an empty string as placeholder
        "userId": 1  # Assuming referenced accounts exist as per instructions, using default userId 1
    }
    
    payload["url"] = inputs.get("new_url")
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create post. Status code: {response.status_code}")
        
    data = response.json()
    
    if not data:
        return None
        
    return data.get("id")