import requests

def solve(inputs):
    """
    Retrieves comments from JSONPlaceholder filtered by postId.
    
    Args:
        inputs (dict): Must contain 'post_identifier' key with an integer value.
        
    Returns:
        list or None: Decoded JSON response if successful, None for empty response.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    post_id = inputs['post_identifier']
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # Return None if the response is empty, otherwise return the list of comments
        return data if data else None
        
    except requests.RequestException as e:
        raise e