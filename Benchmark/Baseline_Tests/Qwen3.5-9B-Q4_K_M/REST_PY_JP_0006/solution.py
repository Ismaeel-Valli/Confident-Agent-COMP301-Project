import requests

def solve(inputs):
    """
    Deletes a post by identifier from JSONPlaceholder.
    
    Args:
        inputs (dict): A dictionary containing 'resource_id' as the post ID to delete.
        
    Returns:
        None if deletion is successful (empty response).
        The decoded JSON response otherwise.
        
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    url = f"https://jsonplaceholder.typicode.com/posts/{resource_id}"
    
    try:
        response = requests.delete(url)
        response.raise_for_status()
        
        if response.status_code == 204:
            return None
        
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP Error occurred while deleting post: {e}")