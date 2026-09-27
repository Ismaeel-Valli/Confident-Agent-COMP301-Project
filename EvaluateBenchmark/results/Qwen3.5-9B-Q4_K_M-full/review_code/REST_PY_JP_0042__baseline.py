import requests

def solve(inputs):
    """
    Retrieves comments from JSONPlaceholder filtered by postId.
    
    Args:
        inputs (dict): A dictionary containing 'post_identifier' key.
        
    Returns:
        list or None: The decoded JSON response (list of comments) if successful, 
                      None if the response is empty.
                      
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    post_id = inputs.get('post_identifier')
    
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    return None if len(data) == 0 else data