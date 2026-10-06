import requests

def solve(inputs):
    """
    Retrieve a post by identifier from JSONPlaceholder and return its title.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int) for the post ID.
        
    Returns:
        str or None: The post's title, or None if absent or response is empty.
        
    Raises:
        requests.exceptions.RequestException: For unsuccessful HTTP responses.
    """
    resource_id = inputs.get('resource_id')
    
    if resource_id is None:
        raise ValueError("Missing 'resource_id' in inputs")
    
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {'id': resource_id}
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return data.get('title')
    else:
        raise requests.exceptions.HTTPError(f"Failed to retrieve post: {response.status_code}")