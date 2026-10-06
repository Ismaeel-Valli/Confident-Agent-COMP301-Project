import requests

def solve(inputs):
    """
    Retrieve a comment by identifier from JSONPlaceholder and return its name value.
    
    Args:
        inputs (dict): Dictionary containing 'resource_id' (int) - the comment ID.
        
    Returns:
        str or None: The 'name' field of the comment, or None if absent or response is empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    resource_id = inputs['resource_id']
    url = "https://jsonplaceholder.typicode.com/comments"
    
    params = {
        'postId': resource_id
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        if not data:
            return None
        
        comment = data[0]
        return comment.get('name')
    else:
        raise requests.RequestException(f"Failed to retrieve comment: {response.status_code}")