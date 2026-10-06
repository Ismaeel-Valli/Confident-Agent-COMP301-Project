import requests

def solve(inputs):
    """
    Updates selected fields of a user in DummyJSON API.
    
    Args:
        inputs (dict): Dictionary containing:
            - resource_id (str): Identifier of the user to update.
            - new_firstName (str): New value for the first name attribute.
    
    Returns:
        str or None: The response's 'id' value if present, otherwise None for a successful empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx).
    """
    resource_id = inputs.get("resource_id")
    new_firstName = inputs.get("new_firstName")
    
    if not resource_id or new_firstName is None:
        raise ValueError("Missing required input fields: resource_id and new_firstName.")

    url = f"https://dummyjson.com/users/{resource_id}"
    payload = {"firstName": new_firstName}
    
    response = requests.put(url, json=payload)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failed to update user. HTTP status code: {response.status_code}, Response: {response.text}")
    
    # DummyJSON returns the updated object on PUT requests, which includes the 'id' field.
    data = response.json()
    
    return data.get("id")