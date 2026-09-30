import requests

def solve(inputs):
    """
    Retrieve comments from JSONPlaceholder filtered by postId.
    
    Args:
        inputs (dict): Must contain 'post_identifier' key with the post ID to filter by.
        
    Returns:
        list or None: The decoded JSON response as a list of comments, or None if the response is empty.
        
    Raises:
        requests.exceptions.HTTPError: If the HTTP response status code indicates an error (4xx or 5xx).
    """
    base_url = "https://jsonplaceholder.typicode.com"
    post_id = inputs["post_identifier"]
    
    url = f"{base_url}/posts/{post_id}/comments"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        if not data:
            return None
            
        return data
        
    except requests.exceptions.HTTPError as e:
        raise