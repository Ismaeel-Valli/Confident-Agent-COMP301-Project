import requests

def solve(inputs):
    """
    Submit a new user to DummyJSON.
    
    Args:
        inputs (dict): Must contain 'new_firstName' key with the first name value.
        
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users/add"
    
    payload = {
        "firstName": inputs["new_firstName"],
        "lastName": "Doe",  # Required field for user creation
        "email": "user@example.com",  # Required field
        "age": 30,  # Optional but commonly included
        "gender": "male",  # Optional
        "phone": "+1234567890",  # Optional
        "image": "https://dummyjson.com/image"  # Optional
    }
    
    response = requests.post(base_url, json=payload)
    
    if response.status_code == 201:
        return None
    elif response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to create user. Status code: {response.status_code}, Response: {response.text}")