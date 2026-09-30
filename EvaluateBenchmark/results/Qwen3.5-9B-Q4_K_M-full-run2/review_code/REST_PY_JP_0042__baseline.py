import requests

def solve(inputs):
    """
    Retrieves comments from JSONPlaceholder filtered by postId.
    
    Args:
        inputs (dict): A dictionary containing 'post_identifier' to filter by postId.
        
    Returns:
        list or None: The decoded JSON response as a list of comments, or None if the response is empty.
        
    Raises:
        requests.RequestException: If the HTTP response is unsuccessful.
    """
    post_id = inputs.get('post_identifier')
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"
    
    response = requests.get(url)
    response.raise_for_status()  # Raises an exception for unsuccessful HTTP responses
    
    data = response.json()
    
    return None if not data else data