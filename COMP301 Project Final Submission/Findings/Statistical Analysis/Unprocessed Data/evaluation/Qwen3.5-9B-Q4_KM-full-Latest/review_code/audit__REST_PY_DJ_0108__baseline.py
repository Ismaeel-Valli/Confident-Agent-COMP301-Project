import requests

def solve(inputs):
    """
    Submits a new user to DummyJSON using the provided email and first name.
    
    Args:
        inputs (dict): A dictionary containing 'new_email' and 'new_firstName'.
        
    Returns:
        int or None: The ID of the newly created user, or None if the response is empty.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    
    payload = {
        "email": inputs["new_email"],
        "firstName": inputs["new_firstName"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise requests.exceptions.RequestException(f"Failed to create user. Status code: {response.status_code}")
    
    if not response.json():
        return None
    
    return response.json().get("id")