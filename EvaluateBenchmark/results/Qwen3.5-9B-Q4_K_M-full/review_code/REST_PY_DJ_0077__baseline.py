import requests

def solve(inputs):
    """
    Updates selected fields of a user in DummyJSON.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'resource_id': Identifier of the user (e.g., '/users/1')
            - 'new_age': The new value for the age attribute
    
    Returns:
        None if the update is successful (empty response).
        The decoded JSON response otherwise.
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful status code.
    """
    resource_id = inputs.get('resource_id')
    new_age = inputs.get('new_age')
    
    # Prepare the payload for the PUT request
    payload = {
        "age": new_age
    }
    
    # Make the PUT request to DummyJSON API
    response = requests.put(f"https://dummyjson.com/users{resource_id}", json=payload)
    
    # Check if the response was successful
    if response.status_code != 200:
        raise Exception(f"Failed to update user. Status code: {response.status_code}, Response: {response.text}")
    
    # Decode and return the JSON response
    return response.json()