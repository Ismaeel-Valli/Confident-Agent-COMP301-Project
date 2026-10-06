import requests

def solve(inputs):
    """
    Updates selected fields of a user in DummyJSON.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'resource_id': Identifier of the user (e.g., '/users/1')
            - 'new_age': The new value for the age attribute
    
    Returns:
        None if the HTTP response is successful and empty.
        The decoded JSON response otherwise.
    
    Raises:
        Exception: If the HTTP response indicates an error (status code >= 400).
    """
    resource_id = inputs['resource_id']
    new_age = inputs['new_age']
    
    # Prepare the payload for the PATCH request
    payload = {
        "age": new_age
    }
    
    # Send the PATCH request to DummyJSON API
    response = requests.patch(f"https://dummyjson.com/users{resource_id}", json=payload)
    
    # Raise an exception for unsuccessful HTTP responses (status code >= 400)
    if response.status_code >= 400:
        raise Exception(f"Failed to update user: {response.text}")
    
    # Return None for a successful empty response
    if not response.text:
        return None
    
    # Decode and return the JSON response
    return response.json()