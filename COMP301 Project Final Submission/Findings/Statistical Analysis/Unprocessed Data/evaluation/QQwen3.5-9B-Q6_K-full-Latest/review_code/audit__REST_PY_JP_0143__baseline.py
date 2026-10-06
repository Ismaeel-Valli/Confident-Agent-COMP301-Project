import requests

def solve(inputs):
    """
    Updates the thumbnailUrl of a photo in JSONPlaceholder and returns its ID.
    
    Args:
        inputs (dict): A dictionary containing:
            - resource_id (int): The ID of the photo to update.
            - new_thumbnailUrl (str): The new URL for the thumbnail.
    
    Returns:
        int or None: The ID of the updated photo, or None if the response is empty.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    resource_id = inputs['resource_id']
    new_thumbnailUrl = inputs['new_thumbnailUrl']
    
    url = f"https://jsonplaceholder.typicode.com/photos/{resource_id}"
    payload = {
        "thumbnailUrl": new_thumbnailUrl
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update photo. Status code: {response.status_code}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data.get('id')