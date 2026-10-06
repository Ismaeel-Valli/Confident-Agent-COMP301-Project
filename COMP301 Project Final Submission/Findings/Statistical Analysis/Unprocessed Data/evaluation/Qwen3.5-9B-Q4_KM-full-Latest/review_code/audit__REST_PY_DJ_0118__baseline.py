import requests

def solve(inputs):
    """
    Submits a new user to DummyJSON using the provided first name and phone number.
    
    Args:
        inputs (dict): A dictionary containing 'new_firstName' and 'new_phone'.
        
    Returns:
        None if the response is empty (successful submission).
        The decoded JSON response otherwise.
        
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    
    payload = {
        "name": inputs.get("new_firstName"),
        "phone": inputs.get("new_phone")
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create user. Status code: {response.status_code}, Response: {response.text}")
    
    # DummyJSON typically returns an empty body for POST requests on /users
    if not response.text.strip():
        return None
    
    return response.json()