import requests

def solve(inputs):
    """
    Submit a new post to JSONPlaceholder using the provided title.
    
    Args:
        inputs (dict): Must contain 'new_title' key with the title value.
        
    Returns:
        str or None: The response's title value, or None if absent or on empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/posts"
    
    payload = {
        "title": inputs["new_title"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create post. Status code: {response.status_code}")
    
    data = response.json()
    
    return data.get("title")