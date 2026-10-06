import requests

def solve(inputs):
    """
    Retrieve an album by identifier from JSONPlaceholder and return its title.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int) - the album ID.
        
    Returns:
        str or None: The album's title, or None if absent or response is empty.
        
    Raises:
        requests.RequestException: If HTTP response is unsuccessful.
    """
    resource_id = inputs.get('resource_id')
    
    if resource_id is None:
        raise ValueError("Missing required 'resource_id' in inputs")
    
    url = "https://jsonplaceholder.typicode.com/albums"
    params = {"id": resource_id}
    
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raises exception for unsuccessful HTTP responses
    
    data = response.json()
    
    if not data:
        return None
    
    title = data.get('title')
    return title if title is not None else None