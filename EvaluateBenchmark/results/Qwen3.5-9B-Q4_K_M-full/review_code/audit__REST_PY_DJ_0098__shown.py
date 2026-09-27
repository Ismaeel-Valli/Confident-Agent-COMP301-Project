import requests

def solve(inputs):
    """
    Submit a new user to DummyJSON.
    
    Args:
        inputs (dict): Contains 'new_email' and 'new_firstName'.
        
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users/add"
    
    payload = {
        "email": inputs["new_email"],
        "firstName": inputs["new_firstName"]
    }
    
    response = requests.post(base_url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create user. Status code: {response.status_code}")
    
    return response.json()