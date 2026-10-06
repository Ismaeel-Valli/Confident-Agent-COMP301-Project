import requests

def solve(inputs):
    """
    Retrieves comments from JSONPlaceholder filtered by postId.
    
    Args:
        inputs (dict): A dictionary containing 'post_identifier' (postId).
        
    Returns:
        list or None: The decoded JSON response as a list of comments, or None if the response is empty.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    post_id = inputs.get('post_identifier')
    
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # Return None if the list is empty, otherwise return the data
        return data if data else None
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to retrieve comments: {e}")