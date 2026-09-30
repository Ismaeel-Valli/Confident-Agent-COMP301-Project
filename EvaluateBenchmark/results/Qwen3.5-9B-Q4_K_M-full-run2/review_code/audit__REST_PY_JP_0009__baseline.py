import requests

def solve(inputs):
    """
    Retrieves a comment by identifier from JSONPlaceholder.
    
    Args:
        inputs (dict): A dictionary containing 'resource_id' as the comment ID.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx range).
    """
    resource_id = inputs['resource_id']
    url = f"https://jsonplaceholder.typicode.com/comments/{resource_id}"
    
    response = requests.get(url)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    return None if data == {} else data