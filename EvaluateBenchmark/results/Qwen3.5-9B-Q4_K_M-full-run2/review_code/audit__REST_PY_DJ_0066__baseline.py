import requests

def solve(inputs):
    """
    Updates selected fields of a user in DummyJSON API.
    
    Args:
        inputs (dict): Contains 'resource_id' and 'new_lastName'.
        
    Returns:
        str or None: The response's 'id' value if present, otherwise None for successful empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    resource_id = inputs.get('resource_id')
    new_last_name = inputs.get('new_lastName')
    
    url = f"https://dummyjson.com/users/{resource_id}"
    
    payload = {
        "lastName": new_last_name
    }
    
    response = requests.patch(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update user. Status code: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    # DummyJSON returns the updated user object on PATCH success
    if 'id' in data:
        return data['id']
    else:
        return None