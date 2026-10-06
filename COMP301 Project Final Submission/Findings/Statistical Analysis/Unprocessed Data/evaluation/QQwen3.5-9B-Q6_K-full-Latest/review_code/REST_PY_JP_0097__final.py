import requests


def solve(inputs):
    """
    Update a photo in JSONPlaceholder with a new URL.
    
    Args:
        inputs (dict): Must contain 'resource_id' and 'new_url'.
        
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs["resource_id"]
    new_url = inputs["new_url"]
    
    url = f"https://jsonplaceholder.typicode.com/photos/{resource_id}"
    payload = {
        "userId": 1,
        "albumId": 1,
        "title": "foo",
        "userStatus": 0,
        "url": new_url,
        "thumbnailUrl": "https://via.placeholder.com/150"
    }
    
    response = requests.put(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    return response.json()