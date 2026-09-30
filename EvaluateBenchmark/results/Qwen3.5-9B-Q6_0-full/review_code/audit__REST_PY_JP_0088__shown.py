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
        str or None: The response's 'name' field, or None if absent or on empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
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
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return data.get("name")
    elif response.status_code in (204,):
        return None
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")