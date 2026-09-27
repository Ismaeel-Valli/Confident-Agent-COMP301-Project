import requests

def solve(inputs):
    """
    Updates selected fields of a user in DummyJSON API.
    
    Args:
        inputs (dict): A dictionary containing:
            - resource_id (str): Identifier of the user.
            - new_username (str): New value for the username attribute.
    
    Returns:
        str or None: The response's 'id' value if present, otherwise None for a successful empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code >= 400).
    """
    resource_id = inputs.get("resource_id")
    new_username = inputs.get("new_username")
    
    url = f"https://httpbin.org/put"
    payload = {
        "resource_id": resource_id,
        "new_username": new_username
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code >= 400:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    # Return 'id' if present in the response JSON, otherwise None for successful empty response
    return response.json().get("id")