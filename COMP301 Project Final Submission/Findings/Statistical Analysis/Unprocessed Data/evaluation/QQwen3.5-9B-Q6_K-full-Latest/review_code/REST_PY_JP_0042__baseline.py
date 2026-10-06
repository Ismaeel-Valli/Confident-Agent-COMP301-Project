import requests

def solve(inputs):
    """
    Retrieves comments from JSONPlaceholder filtered by postId.
    
    Args:
        inputs (dict): Must contain 'post_identifier' key with the post ID to filter by.
        
    Returns:
        list or None: Decoded JSON response if successful, or None for an empty response.
        
    Raises:
        requests.RequestException: If the HTTP response is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    post_id = inputs.get('post_identifier')
    
    if post_id is None:
        raise ValueError("Missing 'post_identifier' in inputs")

    url = f"{base_url}/posts/{post_id}/comments"
    
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
    
    data = response.json()
    
    if not data:
        return None
        
    return data