import requests

def solve(inputs):
    """
    Retrieve comments from JSONPlaceholder filtered by postId.
    
    Args:
        inputs (dict): Must contain 'post_identifier' key with the post ID to filter by.
        
    Returns:
        list or None: Decoded JSON response as a list, or None if empty.
        
    Raises:
        requests.exceptions.RequestException: For unsuccessful HTTP responses.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    post_id = inputs["post_identifier"]
    
    url = f"{base_url}/posts/{post_id}/comments"
    
    response = requests.get(url)
    response.raise_for_status()  # Raises an exception for unsuccessful HTTP responses
    
    data = response.json()
    
    return data if data else None