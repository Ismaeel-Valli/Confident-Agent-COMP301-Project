import requests


def solve(inputs):
    """
    Update a photo in JSONPlaceholder by changing its thumbnailUrl.
    
    Args:
        inputs (dict): Must contain 'resource_id' and 'new_thumbnailUrl'.
        
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    resource_id = inputs["resource_id"]
    new_thumbnail_url = inputs["new_thumbnailUrl"]
    
    url = f"https://jsonplaceholder.typicode.com/photos/{resource_id}"
    
    payload = {
        "thumbnailUrl": new_thumbnail_url
    }
    
    response = requests.put(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    return response.json()