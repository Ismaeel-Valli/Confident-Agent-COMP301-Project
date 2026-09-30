import requests

def solve(inputs):
    """
    Submits a new photo to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'new_thumbnailUrl': The URL for the thumbnail image.
            - 'new_title': The title of the post.
    
    Returns:
        int or None: The ID of the created photo if successful, or None if the response is empty.
    
    Raises:
        requests.RequestException: If the HTTP request fails (non-successful status code).
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    
    payload = {
        "thumbnailUrl": inputs.get("new_thumbnailUrl"),
        "title": inputs.get("new_title")
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise requests.RequestException(f"Failed to create photo. Status code: {response.status_code}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data.get("id")