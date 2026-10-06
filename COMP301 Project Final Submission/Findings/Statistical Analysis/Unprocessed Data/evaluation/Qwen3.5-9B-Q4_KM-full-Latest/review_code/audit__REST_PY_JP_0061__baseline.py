import requests

def solve(inputs):
    """
    Updates selected fields of a todo on JSONPlaceholder and returns the new ID or None.
    
    Args:
        inputs (dict): Contains 'resource_id' (todo ID) and 'new_title' (new title).
        
    Returns:
        int or None: The updated todo's ID, or None if the response is empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    resource_id = inputs['resource_id']
    new_title = inputs['new_title']
    
    url = "https://jsonplaceholder.typicode.com/todos/1"  # Note: JSONPlaceholder uses static IDs, but we'll use the provided ID in the path
    
    payload = {
        "title": new_title
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.patch(url.replace("1", str(resource_id)), json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data.get('id')