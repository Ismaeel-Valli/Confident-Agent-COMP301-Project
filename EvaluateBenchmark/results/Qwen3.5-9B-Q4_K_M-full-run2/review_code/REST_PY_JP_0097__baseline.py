import requests

def solve(inputs):
    """
    Updates the 'url' field of a photo on JSONPlaceholder.
    
    Args:
        inputs (dict): A dictionary containing:
            - resource_id (int): The ID of the photo to update.
            - new_url (str): The new URL value for the photo's url attribute.
    
    Returns:
        None if the request is successful (HTTP 200) and returns an empty body.
        The decoded JSON response if a non-empty response is received.
    
    Raises:
        Exception: If the HTTP response status code indicates failure (non-2xx).
    """
    resource_id = inputs['resource_id']
    new_url = inputs['new_url']
    
    url = "https://jsonplaceholder.typicode.com/photos/1"
    payload = {
        "id": resource_id,
        "userId": 1,
        "title": "foo",
        "albumId": 1,
        "thumbnailUrl": "http://via.placeholder.com/200x200",
        "url": new_url
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code == 200:
        if len(response.text) == 0:
            return None
        return response.json()
    else:
        raise Exception(f"HTTP Error: {response.status_code} - {response.text}")