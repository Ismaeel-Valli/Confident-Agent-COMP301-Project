import requests

def solve(inputs):
    """
    Updates the thumbnailUrl of a photo in JSONPlaceholder.
    
    Args:
        inputs (dict): A dictionary containing:
            - resource_id (int): The ID of the photo to update.
            - new_thumbnailUrl (str): The new URL for the thumbnail.
    
    Returns:
        dict or None: The decoded JSON response if successful, otherwise None.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    resource_id = inputs['resource_id']
    new_thumbnailUrl = inputs['new_thumbnailUrl']
    
    url = f"https://jsonplaceholder.typicode.com/photos/{resource_id}"
    data = {
        "thumbnailUrl": new_thumbnailUrl
    }
    
    response = requests.put(url, json=data)
    
    if response.status_code == 200:
        return None
    else:
        raise Exception(f"Failed to update photo. Status code: {response.status_code}, Response: {response.text}")