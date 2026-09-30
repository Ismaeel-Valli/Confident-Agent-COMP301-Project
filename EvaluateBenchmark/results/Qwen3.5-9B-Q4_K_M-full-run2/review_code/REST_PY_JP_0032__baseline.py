import requests

def solve(inputs):
    """
    Submits a new user to JSONPlaceholder using the provided name.
    
    Args:
        inputs (dict): A dictionary containing 'new_name' for the user's name.
        
    Returns:
        None if the response is empty (successful creation).
        The decoded JSON response otherwise.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    new_name = inputs.get("new_name")
    
    payload = {
        "name": new_name,
        "username": "",
        "email": "",
        "address": {"street": "", "suite": "", "city": "", "zipcode": "", "geo": {"lat": "", "lng": ""}},
        "phone": "",
        "website": "",
        "company": {"name": "", "catchPhrase": "", "bs": ""}
    }

    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create user. Status code: {response.status_code}, Response: {response.text}")
    
    return None