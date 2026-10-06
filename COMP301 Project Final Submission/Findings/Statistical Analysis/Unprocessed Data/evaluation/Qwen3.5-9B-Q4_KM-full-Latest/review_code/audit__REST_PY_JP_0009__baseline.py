import requests

def solve(inputs):
    """
    Retrieves a comment by its identifier from JSONPlaceholder.
    
    Args:
        inputs (dict): A dictionary containing 'resource_id' as the comment ID.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    resource_id = inputs.get('resource_id')
    url = f"https://jsonplaceholder.typicode.com/comments/{resource_id}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data