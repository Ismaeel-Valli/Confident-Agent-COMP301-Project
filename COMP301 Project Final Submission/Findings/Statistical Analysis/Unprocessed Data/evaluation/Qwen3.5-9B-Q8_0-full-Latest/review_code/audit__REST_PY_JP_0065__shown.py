import requests

def solve(inputs):
    """
    Update a user in JSONPlaceholder.
    
    Args:
        inputs (dict): Must contain 'resource_id' and 'new_name'.
        
    Returns:
        int or None: The response's id value, or None if the response is empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    resource_id = inputs['resource_id']
    new_name = inputs['new_name']
    
    url = f"https://jsonplaceholder.typicode.com/users/{resource_id}"
    payload = {
        "name": new_name
    }
    
    response = requests.patch(url, json=payload)
    
    if response.status_code != 200:
        raise requests.RequestException(f"Failed to update user: {response.status_code}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data.get('id')