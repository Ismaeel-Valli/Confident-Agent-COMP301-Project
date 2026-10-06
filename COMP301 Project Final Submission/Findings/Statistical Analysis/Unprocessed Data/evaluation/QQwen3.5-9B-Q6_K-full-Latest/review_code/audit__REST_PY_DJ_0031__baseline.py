import requests

def solve(inputs):
    """
    Updates selected fields of a user in DummyJSON and returns the response's id value,
    or None if that attribute is absent or for a successful empty response.
    Raises an exception for an unsuccessful HTTP response.
    
    Args:
        inputs (dict): A dictionary containing:
            - resource_id (str): Identifier of the user.
            - new_firstName (str): Value for the first name attribute.
    
    Returns:
        str or None: The ID from the response, or None if absent or empty response.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    resource_id = inputs.get('resource_id')
    new_firstName = inputs.get('new_firstName')

    if not resource_id or new_firstName is None:
        raise ValueError("Missing required input fields: resource_id and new_firstName")

    url = f"https://dummyjson.com/users/{resource_id}"
    payload = {"firstName": new_firstName}

    response = requests.put(url, json=payload)

    if response.status_code != 200:
        raise Exception(f"Failed to update user. Status code: {response.status_code}, Response: {response.text}")

    return response.json().get('id')