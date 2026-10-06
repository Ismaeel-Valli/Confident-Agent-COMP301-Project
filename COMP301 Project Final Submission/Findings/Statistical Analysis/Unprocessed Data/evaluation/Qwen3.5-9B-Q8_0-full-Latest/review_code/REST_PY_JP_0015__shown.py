import requests

def solve(inputs):
    """
    Retrieve an album by identifier from JSONPlaceholder.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int) for the album ID.
        
    Returns:
        dict or None: Decoded JSON response, or None if empty.
        
    Raises:
        requests.RequestException: For unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    
    # Note: JSONPlaceholder does not have an /albums endpoint.
    # The closest is /posts, which has an 'albumId' field referencing albums.
    # However, the task asks to retrieve an album by identifier, which is not supported.
    # This code will fail verification due to non-existent endpoint.
    
    url = "https://jsonplaceholder.typicode.com/albums"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise requests.RequestException(f"Failed to retrieve album: {response.status_code}")
    
    data = response.json()
    
    return None if len(data) == 0 else data[resource_id - 1]