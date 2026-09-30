import requests

def solve(inputs):
    """
    Submit a new user to JSONPlaceholder.
    
    Args:
        inputs (dict): Dictionary containing:
            - new_name (str): Value for the name attribute
            - new_username (str): Value for the username attribute
    
    Returns:
        dict or None: Decoded JSON response, or None if successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/users"
    
    payload = {
        "name": inputs["new_name"],
        "username": inputs["new_username"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create user. Status code: {response.status_code}")
    
    return response.json()