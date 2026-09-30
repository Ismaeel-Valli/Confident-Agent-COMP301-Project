import requests

def solve(inputs):
    """
    Retrieve an album by identifier from JSONPlaceholder.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int) - the album ID.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs["resource_id"]
    
    # Note: JSONPlaceholder does not have an albums endpoint.
    # The available endpoints are: posts, comments, users, photos, albums (not present).
    # Since the task assumes referenced resources exist, we'll attempt to use a hypothetical
    # /albums/{id} endpoint which doesn't actually exist on jsonplaceholder.typicode.com.
    
    url = "https://jsonplaceholder.typicode.com/albums"
    params = {"id": resource_id}
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data