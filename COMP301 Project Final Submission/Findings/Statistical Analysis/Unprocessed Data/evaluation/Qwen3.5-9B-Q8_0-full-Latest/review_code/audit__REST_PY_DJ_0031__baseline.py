import requests

def solve(inputs):
    """
    Updates selected fields of a user in DummyJSON API.
    
    Args:
        inputs (dict): Dictionary containing:
            - resource_id (str): Identifier of the user
            - new_firstName (str): New value for the first name attribute
    
    Returns:
        str or None: The response's id value, or None if absent or on successful empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    resource_id = inputs.get('resource_id')
    new_first_name = inputs.get('new_firstName')
    
    if not resource_id or new_first_name is None:
        raise ValueError("Missing required input fields: resource_id and new_firstName")

    url = f"https://dummyjson.com/users/{resource_id}"
    
    payload = {
        "firstName": new_first_name
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update user. Status code: {response.status_code}, Response: {response.text}")
    
    # DummyJSON returns a 200 OK with an empty body for successful updates
    return None