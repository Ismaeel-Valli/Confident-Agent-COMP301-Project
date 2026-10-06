import requests

def solve(inputs):
    """
    Update a todo item in JSONPlaceholder with a new title.
    
    Args:
        inputs (dict): Contains 'resource_id' and 'new_title'.
        
    Returns:
        str or None: The updated title from the response, or None if absent.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    resource_id = inputs['resource_id']
    new_title = inputs['new_title']
    
    url = f"https://jsonplaceholder.typicode.com/todos/{resource_id}"
    payload = {
        "title": new_title
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code}")
    
    return response.json().get('title')