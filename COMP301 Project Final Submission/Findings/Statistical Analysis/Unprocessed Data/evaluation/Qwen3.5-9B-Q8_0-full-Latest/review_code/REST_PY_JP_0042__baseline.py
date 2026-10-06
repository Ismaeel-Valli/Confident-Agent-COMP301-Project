import requests

def solve(inputs):
    """
    Retrieves comments from JSONPlaceholder filtered by postId.
    
    Args:
        inputs (dict): A dictionary containing 'post_identifier' key.
        
    Returns:
        list or None: Decoded JSON response as a list, or None if the response is empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    post_id = inputs.get('post_identifier')
    
    if post_id is None:
        raise ValueError("Missing required 'post_identifier' in inputs")

    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"
    
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
    
    data = response.json()
    
    if not data:
        return None
        
    return data