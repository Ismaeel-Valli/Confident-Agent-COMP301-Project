import requests

def solve(inputs):
    """
    Update a comment in JSONPlaceholder.
    
    Parameters:
        inputs (dict): Must contain 'resource_id' and 'new_name'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty body.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    resource_id = inputs['resource_id']
    new_name = inputs['new_name']
    
    url = f"https://jsonplaceholder.typicode.com/comments/{resource_id}"
    
    payload = {
        "name": new_name
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    return response.json() if response.content else None