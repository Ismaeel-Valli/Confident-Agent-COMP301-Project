import requests

def solve(inputs):
    """
    Submits a new user to DummyJSON with provided first name and phone number.
    
    Args:
        inputs (dict): A dictionary containing 'new_firstName' and 'new_phone'.
        
    Returns:
        int or None: The ID of the newly created user, or None if the response is empty.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    
    payload = {
        "name": inputs.get("new_firstName"),
        "phone": inputs.get("new_phone")
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create user. Status code: {response.status_code}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data.get("id")