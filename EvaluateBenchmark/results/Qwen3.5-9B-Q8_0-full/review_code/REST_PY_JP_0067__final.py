import requests

def solve(inputs):
    """
    Retrieve a post by identifier from JSONPlaceholder and return its title.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int) for the post ID.
        
    Returns:
        str or None: The post's title, or None if absent or response is empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    resource_id = inputs.get('resource_id')
    
    if resource_id is None:
        raise ValueError("Missing 'resource_id' in inputs")
    
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {'id': resource_id}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad status codes
        
        data = response.json()
        
        # Check if the response is empty or lacks a 'title' field
        if not data or 'title' not in data:
            return None
            
        return data['title']
        
    except requests.RequestException as e:
        raise