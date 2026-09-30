import requests

def solve(inputs):
    """
    Update selected fields of a user on DummyJSON.
    
    Args:
        inputs (dict): Must contain 'resource_id' and 'new_email'.
        
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    new_email = inputs['new_email']
    
    url = f"https://dummyjson.com/users/{resource_id}"
    payload = {"email": new_email}
    
    response = requests.put(url, json=payload)
    
    if response.status_code == 200:
        return None
    elif response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Failed to update user. Status code: {response.status_code}")