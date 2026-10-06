import requests


def solve(inputs):
    """
    Replace a user record in JSONPlaceholder with supplied data.
    
    Inputs:
        resource_id (int): Identifier of the user to update.
        new_email (str): New email value.
        new_name (str): New name value.
        new_phone (str): New phone value.
        new_username (str): New username value.
        new_website (str): New website value.
    
    Returns:
        int or None: The response's id if present, otherwise None.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/users/{inputs['resource_id']}"
    
    payload = {
        "email": inputs["new_email"],
        "name": inputs["new_name"],
        "phone": inputs["new_phone"],
        "username": inputs["new_username"],
        "website": inputs["new_website"]
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code < 200 or response.status_code >= 400:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    if data is None:
        return None
    
    return data.get("id")