import requests

def solve(inputs):
    """
    Updates selected fields of a user in DummyJSON API.
    
    Args:
        inputs (dict): Contains 'resource_id' (user ID) and 'new_lastName' (new last name).
        
    Returns:
        str or None: The response's id value if present, otherwise None for successful empty response.
        Raises: Exception for unsuccessful HTTP responses.
    """
    resource_id = inputs.get('resource_id')
    new_last_name = inputs.get('new_lastName')
    
    if not resource_id or new_last_name is None:
        raise ValueError("Missing required inputs: resource_id and new_lastName")

    url = f"https://dummyjson.com/users/{resource_id}"
    payload = {"lastName": new_last_name}
    
    try:
        response = requests.put(url, json=payload)
        response.raise_for_status()
        
        if response.status_code == 204:
            return None
        
        data = response.json()
        return data.get('id')
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Failed to update user: {e}")