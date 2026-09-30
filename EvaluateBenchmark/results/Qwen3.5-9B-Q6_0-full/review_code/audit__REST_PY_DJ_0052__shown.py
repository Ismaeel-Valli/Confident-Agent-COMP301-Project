import requests

def solve(inputs):
    """
    Submit a new user to DummyJSON using the provided first and last name.
    
    Args:
        inputs (dict): Must contain 'new_firstName' and 'new_lastName'.
        
    Returns:
        dict or None: Decoded JSON response, or None if response is empty.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/users/add"
    
    payload = {
        "firstName": inputs["new_firstName"],
        "lastName": inputs["new_lastName"]
    }
    
    response = requests.post(base_url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create user. Status code: {response.status_code}")
    
    return response.json()